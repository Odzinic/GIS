'''Imports'''
import numpy as np
import scipy as sp                                                                    # NumPy used for creating arrays 
import os
import time
from osgeo import gdal
from osgeo import gdalconst
import datetime
import math

from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

import matplotlib
import matplotlib.pyplot as plt

gdal.AllRegister()
dr = gdal.GetDriverByName("GTiff")

'''Directories'''
dir = os.getcwd();                                                                      # Directory of the script
fn = os.path.join(dir, "images")                                                        # Directory of the image folder
oput = os.path.join(dir, "output")
final = os.path.join(dir, "output", "result.tif")                                      # Resulting image

if (os.path.exists(fn)):
    next
else:
    os.mkdir(fn)
if (os.path.exists(oput)):
    next
else:
    os.mkdir(oput)


'''Image variables'''
image_files = os.listdir(fn)                                                            # Your list of images
temp_image = gdal.Open(os.path.join(os.path.join(fn + "\{0}".format(image_files[0]))))  # Load the first image to find the information of timeseries
image_width = temp_image.RasterXSize                                                   # Image width in pixels
image_length = temp_image.RasterYSize                                                   # Image length in pixels
img_stack = np.empty((image_length, image_width, len(image_files)), np.dtype('f'))      # Create empty array for values, dtype should be set to 'f' for float
result_raster = np.empty((image_length, image_width), np.dtype('f'))
date = []
temp_image = None

print "This image is {0} by {1}".format(image_width, image_length)

for i, fname in enumerate(image_files):
    dateString = fname.split("_")[0]
    dateConv = datetime.datetime(int(dateString[0:4]),
                                 int(dateString[4:6]),
                                 int(dateString[6:])) - datetime.datetime(int(dateString[0:4]), 1, 1) 
    print str(dateConv)                         
    date.append(float(str(dateConv)[0: str(dateConv).index(" ")]))
date = np.array(date)

'''Loop that loads images into a stack'''
for i, fname in enumerate(image_files):
    img = gdal.Open(os.path.join(fn + ("\{0}".format(fname)))).ReadAsArray()            # Reads an image into an array
    print ("Read {0}. The image is {1} by {2}".format(fname, 
                                                      image_width, image_length))       # Prints confirmation that image was read and its dimensions
    

    
    img_stack[:, :, i] = img                                                            # Stores the image array into a stack
    img = None                                                                          # Clears the loaded array to reduce memory usage

##Define function
def func (x, a, b, c, d):
    return d + c/(1+np.exp(a-b*x))

newX = np.linspace(date[0], date[-1], (date[-1] - date[0]) + 1)

for x in range(image_length):
    for y in range(image_width):
        lai = img_stack[x, y]
        f2 = interp1d(date, lai, kind='cubic')
        newY = f2(newX)
        
        cumLAI = np.trapz(newY,newX)
#        p0 =  (0.1, 0, 0, 7)
#        popt, pcov = curve_fit(func, date, lai, p0)
#        popt = np.empty((4))
#        yEXP = func(trialX, *popt)
#        
#        a1 = popt[0]
#        b1 = popt[1]
#        c1 = popt[2]
#        d1 = popt[3]
#        
#        yMax = (yEXP.max())
#        SOSv = 0.5*yMax
        
#        SOSd = (a1-np.log((c1/(SOSv-d1))-1))/b1
#        print SOSd

        result_raster[x, y] = cumLAI

output_raster = dr.Create(final, image_width, image_length, 1, gdal.GDT_Float32)        # Creates a raster with the dimensions of the timeseries images
output_raster.GetRasterBand(1).WriteArray(result_raster)                                      # Writes the maximum values to the raster
        
        
        
        
        
        
        
        
        