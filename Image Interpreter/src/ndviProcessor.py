
'''Imports'''
import arcpy
import arcpy.sa as arcsa
import numpy as np
#import scipy as sp                                                                    # NumPy used for creating arrays
import os

import time
import datetime
import math
import types
import mpfit



from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

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
tmpImg = None

date = []

imgStack = np.empty((imageHeight, imageWidth, len(lisImages)), np.dtype('int16'))
 
startTime = time.time()
for i, img in enumerate(lisImages):
    
    dateString = img.split(".")[3]
    date.append(int(dateString[4:]))
                                    
#     # Max NDVI !! Will need to loop through series !!
    imgStack[:, :, i] = arcpy.RasterToNumPyArray(os.path.join(imageDir, img), arcpy.Point(rasterExtentX, rasterExtentY),
                                         "", "", -9999)
#     tmp = 0
#    
#     for x in range(imageWidth):
#         for y in range(imageHeight):
#             if (imgStack[x, y, i]  != tmp):
#                 print imgStack[x, y, i]
#                 tmp = imgStack[x, y, i]
#imgStack[imgStack<0] = 0
imgStack[:, :][imgStack[:, :]< 0] = 0
endTime = time.time()
print "Took {0} to load images".format(endTime - startTime)
#maxNDVI = arcpy.NumPyArrayToRaster(np.amax(imgStack, 2)).save(os.path.join(outDir, "maxNDVI.tif"))
# maxNDVI =  np.amax(imgStack[:, :, i])
# print maxNDVI

date = np.array(date)

''' SoS '''

def func (x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))

popt = np.empty((4))
p0 =  [1., 0., 1.]

newX = np.linspace(date[0], date[-1], (date[-1] - date[0]) + 1)

for x in range(imageHeight):
    for y in range(imageWidth):
        lai = imgStack[x, y]
        if (np.count_nonzero(lai) > 3):
            try:
                popt, pcov = curve_fit(func, date, lai, p0)

            except RuntimeError:
                print("Error - curve_fit failed")
            f2 = interp1d(date, lai, kind='cubic')
            newY = f2(newX)
            print newY
        
            yEXP = func(newX, *popt)

            a1 = popt[0]
            b1 = popt[1]
            c1 = popt[2]
        #d1 = popt[3]
        
        
        #Plot the figure
            fig1 = plt.figure()
            #plt.plot(date, lai, label='Data', ls='none', marker='o')
            plt.plot(newX, f2(newX), 'r-',ls='--', label="Interpolated")
#        plt.plot(newX, newY, 'r-',ls='--', label="Cubic")
            #plt.plot(newX, yEXP, 'r-',ls='none', marker = '*',label="EXP")
        ##plt.plot(doy, lai,'o',newX,f(newX),'-', newX, f2(trailX),'--')
        ##plt.legend(['data', 'linear', 'cubic'], loc='best')
            fig1.show()
            time.sleep(3)
            plt.close(fig1)







