import os
import urllib.request
from urllib.parse import urlparse
import csv
import time
import datetime
from numpy import loadtxt
import numpy as np
import h5py
import csv
import sys
import gdal, ogr, os, osr
import smtplib
from email.mime.text import MIMEText
import socket

def getCurrentDirectory():
	return(os.path.dirname(os.path.realpath(__file__)) + '/')

def getTimeStamp():
	return(time.strftime("%Y%m%d-%H%M%S"))

# def getGPMDownloadTime():
	# return(datetime.datetime.utcnow() - datetime.timedelta(hours=9))
	
def getDownloadURL():
	downloadString = time.strftime('%Y%m')
	return('ftp://aakash.ahamed@nasa.gov:aakash.ahamed@nasa.gov@jsimpson.pps.eosdis.nasa.gov/NRTPUB/imerg/early/' + downloadString + '/')

def getFileList(timeStr):
	urllib.request.urlretrieve(getDownloadURL(),getCurrentDirectory() + timeStr + '.txt')

def readTextFile(filename,dataType,delim):
	return(loadtxt(getCurrentDirectory() + filename +'.txt',dtype=dataType,delimiter=delim))
	
def downloadMostRecent(fileNameLength):
	getFileList(timeStr)
	filelist = readTextFile(timeStr,'str',',')
	filename=filelist[-1]
	filename=filename[-(fileNameLength+1):-1]
	urllib.request.urlretrieve(getDownloadURL() + filename, getCurrentDirectory() + timeStr + '.h5')
	os.remove(getCurrentDirectory() + timeStr + '.txt')
	return(filename)

def readHDF5Variables():
	gpmhdf = h5py.File(getCurrentDirectory() + timeStr + '.h5', 'r')
	precipitationCal = gpmhdf['Grid']['precipitationCal'][2600:2683,1163:1205]
	lat = gpmhdf['Grid']['lat'][1163:1205]
	lon = gpmhdf['Grid']['lon'][2600:2683]
	gpmhdf.close()
	try:
		sumNewData(precipitationCal)
	except:
		saveTextFile(timeStr[-11:-7],precipitationCal)
	return(lat,lon)
	
def saveTextFile(saveName,variableName):
	np.savetxt(getCurrentDirectory() + saveName + '.txt',variableName,delimiter=',')
	try: 
		os.remove(getCurrentDirectory() + timeStr + '.h5')
	except:
		print(' ')

def sumNewData(newData):
	todayData = readTextFile(timeStr[-11:-7],'float',',')
	todayData=np.asarray(todayData)
	#todayData=todayData.astype(float)
	summedData=todayData + newData
	saveTextFile(timeStr[-11:-7],summedData)

# Untested from here: 
	
def PctChange(newData):
	TRMM_thresholds=readTextFile('Annual_Thresholds','float','\t')
	TRMM_thresh=np.asarray(TRMM_thresholds)
	#TRMM_thresh=TRMM_thresh # MYSTERY 
	P_change=((np.subtract(newData,TRMM_thresh))/TRMM_thresh)*100
	masked_change = mask(P_change)
	return(masked_change)

	
def mask(inputArray):
	NPL_mask=readTextFile('Nepal_Mask_f','float','\t')
	NPL_mask=np.asarray(NPL_mask)
	finmask=(inputArray*NPL_mask)
	finmask[np.isnan(finmask)] =-9999.9
	finmask[finmask<-1000] = -9999.9
	saveTextFile(timeStr,finmask)
	return(finmask)
	
	

def array2raster(newRasterfn,rasterOrigin,pixelWidth,pixelHeight,array):

    cols = array.shape[1]
    rows = array.shape[0]
    originX = rasterOrigin[0]
    originY = rasterOrigin[1]
    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Byte)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG (4326) #(32645)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()
	
def getNepalExtent():
	data = gdal.Open('./referenceFile/reference.tif')
	geoTransform = data.GetGeoTransform()
	minx = geoTransform[0]
	maxy = geoTransform[3]
	maxx = minx + geoTransform[1]*data.RasterXSize
	miny = maxy + geoTransform[5]*data.RasterYSize
	extent=[minx,maxx,miny,maxy]
	return(extent)
		
def main():
	global timeStr
	timeStr=getTimeStamp()
	fileNameLength = len('3B-HHR-E.MS.MRG.3IMERG.20150625-S080000-E082959.0480.V03E.RT-H5')
	current_file = downloadMostRecent(fileNameLength)
	print(current_file)
	latitude,longitude=readHDF5Variables()
	if '.0630.' in current_file:
		max_lat=latitude[latitude.shape[0]-1]
		min_lat=latitude[0]
		max_lon=longitude[longitude.shape[0]-1]
		min_lon=longitude[0]
		ysize=(max_lat-min_lat)/latitude.shape[0]
		xsize=(max_lon-min_lon)/longitude.shape[0]
		masked_change = PctChange(readTextFile(timeStr[-11:-7],'float',','))
		reverse_mask = np.rot90(masked_change) # reverse array so the tif looks like the array
		extent=getNepalExtent()
		array2raster('./TIFFout/' + timeStr + '.tif',[extent[0],extent[2]],xsize,ysize,reverse_mask)

if __name__ == "__main__":
    main()
