# Download FTP data from Server
import sys
import re
import os
import urllib.request
from urllib.parse import urlparse
import csv


# url names
tifurl = 'ftp://aakash.ahamed@nasa.gov:aakash.ahamed@nasa.gov@jsimpson.pps.eosdis.nasa.gov/NRTPUB/imerg/gis/early/3B-HHR-E.MS.MRG.3IMERG.20150625-S113000-E115959.0690.V03E.30min.tif'
hdfurl = 'ftp://aakash.ahamed@nasa.gov:aakash.ahamed@nasa.gov@jsimpson.pps.eosdis.nasa.gov/NRTPUB/imerg/early/201506/3B-HHR-E.MS.MRG.3IMERG.20150625-S080000-E082959.0480.V03E.RT-H5'
tifdirurl = 'ftp://aakash.ahamed@nasa.gov:aakash.ahamed@nasa.gov@jsimpson.pps.eosdis.nasa.gov/NRTPUB/imerg/gis/early/'
dirurl = 'ftp://aakash.ahamed@nasa.gov:aakash.ahamed@nasa.gov@jsimpson.pps.eosdis.nasa.gov/NRTPUB/imerg/early/201506/' 

# DLING list of available files to directory
list = urllib.request.urlretrieve(dirurl,'C:/Users/aahamed/Desktop/GPM_files/gpm.txt')

#Picking last file
stringlength = len('3B-HHR-E.MS.MRG.3IMERG.20150625-S080000-E082959.0480.V03E.RT-H5')

# Reading txt file
f = open('C:/Users/aahamed/Desktop/gpm.txt','r')
filelist = f.read()

#Specifying desired file
filename = filelist[-(stringlength+1):]

# Downloading last file
HDF = urllib.request.urlretrieve(dirurl+filename,'C:/Users/aahamed/Desktop/test.h5')
# print(HDF)

# reading structs from hdf 5
import h5py
hdf5_file_name='C:/Users/aahamed/Desktop/test.h5'
gpmhdf = h5py.File(hdf5_file_name, 'r')   # 'r' means that hdf5 file is open in read-only mode
print (gpmhdf)

# Specifying nepal area
precipitation = gpmhdf['Grid']['precipitationCal'][2611:2720, 1153:1197]
lat = gpmhdf['Grid']['lat'][1153:1197]
long = gpmhdf['Grid']['lon'][2611:2720]

print(precipitation.shape)

