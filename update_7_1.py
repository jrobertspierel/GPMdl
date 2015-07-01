# Download FTP data from Server
import sys
import re
import os
import urllib.request
from urllib.parse import urlparse
import csv
import time
import datetime
import numpy as np


# url names
tifurl = 'ftp://aakash.ahamed@nasa.gov:aakash.ahamed@nasa.gov@jsimpson.pps.eosdis.nasa.gov/NRTPUB/imerg/gis/early/3B-HHR-E.MS.MRG.3IMERG.20150625-S113000-E115959.0690.V03E.30min.tif'
hdfurl = 'ftp://aakash.ahamed@nasa.gov:aakash.ahamed@nasa.gov@jsimpson.pps.eosdis.nasa.gov/NRTPUB/imerg/early/201506/3B-HHR-E.MS.MRG.3IMERG.20150625-S080000-E082959.0480.V03E.RT-H5'
tifdirurl = 'ftp://aakash.ahamed@nasa.gov:aakash.ahamed@nasa.gov@jsimpson.pps.eosdis.nasa.gov/NRTPUB/imerg/gis/early/'
dirurl = 'ftp://aakash.ahamed@nasa.gov:aakash.ahamed@nasa.gov@jsimpson.pps.eosdis.nasa.gov/NRTPUB/imerg/early/'+time.strftime('%Y%m')+'/'

#Time Stamping
current_time=datetime.datetime.utcnow()
GPM_time=current_time - datetime.timedelta(hours=9)	
print (GPM_time)

# Dynamically name files with timestamp
timestr = time.strftime("%Y%m%d-%H%M%S")

# DLING list of available files to directory
list = urllib.request.urlretrieve(dirurl,'C:/Users/aahamed/Desktop/GPM_files/'+timestr+'.txt')

#Picking last file
stringlength = len('3B-HHR-E.MS.MRG.3IMERG.20150625-S080000-E082959.0480.V03E.RT-H5')

# Reading txt file
f = open('C:/Users/aahamed/Desktop/GPM_files/' + timestr +'.txt','r')
filelist = f.read()

#Specifying desired file
filename = filelist[-(stringlength+1):]

# Downloading last file
HDF = urllib.request.urlretrieve(dirurl+filename,'C:/Users/aahamed/Desktop/GPM_files/'+timestr+'.h5')
# print(HDF)

# reading structs from hdf 5
import h5py
hdf5_file_name='C:/Users/aahamed/Desktop/GPM_files/20150629-143000.h5'
gpmhdf = h5py.File(hdf5_file_name, 'r')   # 'r' means that hdf5 file is open in read-only mode
print (gpmhdf)

# Specifying nepal area
precipitation1 = gpmhdf['Grid']['precipitationCal'][2600:2682 , 1163:1204]
lat1 = gpmhdf['Grid']['lat'][1163:1204]
long1 = gpmhdf['Grid']['lon'][2600:2682]

print(np.max(precipitation1))

# Writing array as textfile
import csv
np.savetxt('C:/Users/aahamed/Desktop/GPM_files/file1.txt',precipitation1,delimiter=',')

f = open('C:/Users/aahamed/Desktop/GPM_files/file1.txt','r')
prev_sum = f.read()
prev_sum=np.asarray(prev_sum)
prev_sum=prev_sum.astype(float)

# Second file
hdf5_file_name2='C:/Users/aahamed/Desktop/GPM_files/20150630-172840.h5'
gpmhdf2 = h5py.File(hdf5_file_name2, 'r')   # 'r' means that hdf5 file is open in read-only mode
print (gpmhdf2)

precipitation2 = gpmhdf2['Grid']['precipitationCal'][2600:2682 , 1163:1204]
lat2 = gpmhdf2['Grid']['lat'][1163:1204]
long2 = gpmhdf2['Grid']['lon'][2600:2682]

tot_sum= (precipitation2+prev_sum)
print(tot_sum)
