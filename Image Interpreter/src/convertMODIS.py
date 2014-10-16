
'''Imports'''
import arcpy
import arcpy.sa as arcsa
import numpy as np
#import scipy as sp                                                                    # NumPy used for creating arrays
import os
import glob
import fnmatch

import time
import datetime
import math
import types


# from scipy.optimize import curve_fit
# from scipy.interpolate import interp1d

import matplotlib
import matplotlib.pyplot as plt

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension('spatial')

'''Directories'''
mainDir = os.getcwd();                                                                      # Directory of the script
imageDir = os.path.join(mainDir, "images")                                                      # Directory of the image folder
outDir = os.path.join(mainDir, "output")

if (os.path.exists(outDir)):
    next
else:
    os.mkdir(outDir)

lisImages = filter((lambda x: x.endswith('.tif')), os.listdir(imageDir))
tmpImg = arcpy.Raster(os.path.join(imageDir, lisImages[0]))
imageWidth = tmpImg.width
imageHeight = tmpImg.height
## MIGHT NEED TO COPY METADATA
#del tmpImg

dsc=arcpy.Describe(tmpImg)
arcpy.env.outputCoordinateSystem=dsc.SpatialReference

rasterExtentX = tmpImg.extent.XMin
rasterExtentY = tmpImg.extent.YMin

rasterXCellSize = tmpImg.meanCellWidth
rasterYCellSize = tmpImg.meanCellHeight





outArray = np.empty((imageHeight, imageWidth), np.dtype('int16'))
inArray = np.empty((imageHeight, imageWidth), np.dtype('float32'))

for img in lisImages:
        
    array = arcpy.RasterToNumPyArray(os.path.join(imageDir, img), arcpy.Point(rasterExtentX, rasterExtentY),
                                         "", "")
                                         
    array = np.multiply(array, 10000)
    outArray = array.astype(int)
    outArray[outArray<0] = -9999
    outArray = arcpy.NumPyArrayToRaster(outArray, "", "", "", -9999).save(os.path.join(imageDir, img))
     
    array = None
    print "{0} converted".format(img)











