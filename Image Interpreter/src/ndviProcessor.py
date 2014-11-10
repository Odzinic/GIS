
'''Imports'''
import arcpy
import arcpy.sa as arcsa
import numpy as np
#import scipy as sp                                                                    # NumPy used for creating arrays
import os

import time
import datetime
import math

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
sosdayRaster = np.zeros((imageHeight, imageWidth), np.dtype('int16'))
eosdayRaster = np.zeros((imageHeight, imageWidth), np.dtype('int16'))
sosndviRaster = np.zeros((imageHeight, imageWidth), np.dtype('float32'))
eosndviRaster = np.zeros((imageHeight, imageWidth), np.dtype('float32'))
maxdayRaster = np.zeros((imageHeight, imageWidth), np.dtype('int16'))
maxndviRaster = np.zeros((imageHeight, imageWidth), np.dtype('float32'))
seasdurRaster = np.zeros((imageHeight, imageWidth), np.dtype('int16'))
seasampRaster = np.zeros((imageHeight, imageWidth), np.dtype('float32'))
seasintegRaster = np.zeros((imageHeight, imageWidth), np.dtype('float32'))
seaspasgRaster = np.zeros((imageHeight, imageWidth), np.dtype('float32'))

startTime = time.time()
for i, img in enumerate(lisImages):
    
    dateString = img.split(".")[3]
    date.append(int(dateString[4:]))
                                    
#     # Max NDVI !! Will need to loop through series !!
    imgStack[:, :, i] = arcpy.RasterToNumPyArray(os.path.join(imageDir, img), arcpy.Point(rasterExtentX, rasterExtentY),
                                         "", "", -9999)

imgStack[:, :][imgStack[:, :]< 0] = 0
endTime = time.time()
print "Took {0} to load images".format(endTime - startTime)


date = np.array(date)
maxDay = 0
maxNDVI = 0
sosNDVI = 0
sosDay = 0

''' SoS '''

def func(x, *p):
    A, mu, sigma = p
    return A * np.exp(-(x-mu)**2/(2.*sigma**2))

def findX(y, *p):
    A, mu, sigma = p
    return (-1 * math.sqrt((-1 * math.log(y/A)) * (2 * sigma**2))) + mu

def dbl_logistic_model ( p, agdd ):
    """A double logistic model, as in Sobrino and Juliean, or Zhang et al"""
    return p[0] + p[1]* ( 1./(1+np.exp(p[2]*(agdd-p[3]))) + \
                          1./(1+np.exp(-p[4]*(agdd-p[5])))  - 1 )
def log_fit(x, a, b):
    return a + (b * math.log(x))

def findIndex(lst, val):
    return min(enumerate(lst), key=lambda x: abs(x[1]-val))[0]

popt = np.empty((3))
p0 = [.7869, 202., 39.0803]     #1., 70., 10.
newX = np.linspace(date[0], date[-1], (date[-1] - date[0]) + 1)

count = 0

for x in range(imageHeight):
    for y in range(imageWidth):
        lai = imgStack[x, y]
        filtY = np.where(lai == 0)[0]
        lai = np.delete(lai, filtY, 0)
        newdate = np.delete(date, filtY, 0)
        
        try:
            popt, pcov = curve_fit(func, newdate, lai, p0)
            yFit = func(newX, *popt)
            maxDay = popt[1]
            maxNDVI = popt[0]
            sosNDVI = yFit[0] + ((maxNDVI - yFit[0]) * 0.40)
            sosDay = findX(sosNDVI, *popt)
            sosIndex = findIndex(yFit, sosNDVI)
            eosNDVI = yFit[-1] + ((maxNDVI - yFit[-1]) * 0.40)
            revFit = yFit[::-1][:20]                                                            # Check if last 20 days can actually work
            eosIndex = (len(yFit) - 1) - findIndex(revFit, eosNDVI)
            eosDay = newX[eosIndex]
            seasDur = eosDay - sosDay
            seasAmp = maxNDVI - sosNDVI
            seasInteg = np.trapz(yFit[sosIndex:eosIndex], newX[sosIndex:eosIndex])
            seasPASG = sum(yFit[sosIndex:eosIndex] - sosNDVI)
             
        except RuntimeError:
            pass
                  
        except TypeError:
            pass
                                   
        sosdayRaster[x, y] = sosDay
        eosdayRaster[x, y] = eosDay
        sosndviRaster[x, y] = sosNDVI / 10000
        eosndviRaster[x, y] = eosNDVI / 10000
        maxdayRaster[x, y] = maxDay
        maxndviRaster[x, y] = maxNDVI / 10000
        seasdurRaster[x, y] = seasDur
        seasampRaster[x, y] = seasAmp / 10000
        seasintegRaster[x, y] = seasInteg / 10000
        seaspasgRaster[x, y] = seasPASG / 10000
     
        
        
        
        
        
        
        
        #Plot the figure
#         fig1 = plt.figure()
        #plt.plot(date, peval(lai, m.params), label='Fit')
#         plt.plot(newdate, lai, 'r-',ls='--', marker = 'D', label="Interpolated")
# #        plt.plot(newX, newY, 'r-',ls='--', label="Cubic")
#         plt.plot(newX, yFit, 'g-',ls='none', marker = '*',label="EXP")
#         plt.plot(np.array(sosDay), np.array(sosNDVI), 'y-', ls = 'none', marker = 'D')
#         plt.plot(np.array(eosDay), np.array(eosNDVI), 'y-', ls = 'none', marker = 'D')
        #plt.plot(np.array(eosDay), np.array(eosNDVI), 'y-', ls = 'none', marker = 'D')
        ##plt.plot(doy, lai,'o',newX,f(newX),'-', newX, f2(trailX),'--')
#         plt.legend(['data', 'fitted data', 'start of season'], loc='best')
#         plt.xlabel("Day of year")
#         plt.ylabel("NDVI scaled up by a factor of 10000")
#         fig1.show()
        #plt.savefig(r"E:\Omar\Github_Temp\Gtemp\Image Interpreter\src\figures\{0}.png".format(count), format = "png")
#         time.sleep(3)
#         plt.close(fig1)

        
arcpy.NumPyArrayToRaster(sosdayRaster).save(os.path.join(outDir, "SOS_Day.tif"))
arcpy.NumPyArrayToRaster(eosdayRaster).save(os.path.join(outDir, "EOS_Day.tif"))
arcpy.NumPyArrayToRaster(sosndviRaster).save(os.path.join(outDir, "SOS_NDVI.tif"))
arcpy.NumPyArrayToRaster(eosndviRaster).save(os.path.join(outDir, "EOS_NDVI.tif"))
arcpy.NumPyArrayToRaster(maxdayRaster).save(os.path.join(outDir, "MAX_Day.tif"))
arcpy.NumPyArrayToRaster(maxndviRaster).save(os.path.join(outDir, "MAX_NDVI.tif"))
arcpy.NumPyArrayToRaster(seasdurRaster).save(os.path.join(outDir, "SEAS_Duration.tif"))
arcpy.NumPyArrayToRaster(seasampRaster).save(os.path.join(outDir, "SEAS_Amplitude.tif"))
arcpy.NumPyArrayToRaster(seasintegRaster).save(os.path.join(outDir, "SEAS_Integrated.tif"))
arcpy.NumPyArrayToRaster(seaspasgRaster).save(os.path.join(outDir, "SEAS_PASG.tif"))


finalTime = time.time()
print "Total time is {0}".format((finalTime - startTime) / 60)     

