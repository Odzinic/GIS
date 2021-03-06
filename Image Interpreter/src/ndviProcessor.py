
'''Imports'''
import arcpy
import numpy as np                                                                          # NumPy used for creating arrays
import os
import time
import datetime
import math
import zipfile
import scipy
from scipy.optimize import curve_fit
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize.minpack import fsolve

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension('spatial')
np.seterr(all='ignore')


''

'''Directories'''
mainDir = os.getcwd();                                                                      # Directory of the script
archiveDir = r'E:\Omar\MODIS Pheno\Test'
convertDir = os.path.join(mainDir, "convert")
imageDir = os.path.join(mainDir, "images")                                                  # Directory of the image folder
tmpDir = os.path.join(mainDir, "temp")                                                      # Temporary directory for image tiling
tmpoutDir = os.path.join(tmpDir, "out")                                                     # Temporary directory for results of tiled rasters
outDir = os.path.join(mainDir, "output")                                                    # Output directory


'''Check if output directory exists and create one if not'''
if (os.path.exists(outDir)):
    next
else:
    os.mkdir(outDir)
    
if (os.path.exists(tmpDir)):
    next
else:
    os.mkdir(tmpDir)
    


'''Constants'''
lisZips = os.listdir(archiveDir)
sosConst = 0.40
eosConst = 0.40




'''Extracts images from zipped archives'''
print "Extracting rasters from archives"

for zipImg in lisZips:
    f = os.path.join(archiveDir, zipImg)
     
    with zipfile.ZipFile(f, "r") as z:
        z.extractall(convertDir)
print "Extraction complete"




'''Converts MODIS images from 32 bit float to 16 bit int'''
print "Converting images to 16 bit integer format"

convImages = filter((lambda x: x.endswith('.tif')), os.listdir(convertDir))                 # List of images to convert
tmpImg = arcpy.Raster(os.path.join(convertDir, convImages[0]))                              # Load a temp image to fetch metadata and height/width
imageWidth = tmpImg.width                                                                   # Width of images
imageHeight = tmpImg.height                                                                 # Height of images

dsc=arcpy.Describe(tmpImg)
arcpy.env.outputCoordinateSystem=dsc.SpatialReference

rasterExtentX = tmpImg.extent.XMin
rasterExtentY = tmpImg.extent.YMin

rasterXCellSize = tmpImg.meanCellWidth
rasterYCellSize = tmpImg.meanCellHeight


outArray = np.empty((imageHeight, imageWidth), np.dtype('int16'))                           # Creates empty array to contain converted values
inArray = np.empty((imageHeight, imageWidth), np.dtype('float32'))                          # Creates empty array to contain the loaded float values


''' Perform conversion on images '''
for img in convImages:
        
    array = arcpy.RasterToNumPyArray(os.path.join(convertDir, img),                         # Loads raster into array
                                     arcpy.Point(rasterExtentX, rasterExtentY),"", "")
                                         
    array = np.multiply(array, 10000)                                                       # Multiplies each value by 10000
    outArray = array.astype(int)                                                            # Converts data type from float to int
    outArray[outArray<0] = -9999                                                            # Makes all data negative and NoData values 0
    outArray = arcpy.NumPyArrayToRaster(outArray, "", "", "", 
                                        -9999).save(os.path.join(imageDir, img))            # Loads converted values into array of ints and saves to 
                                                                                            # output
     
    array = None
    print "{0} converted".format(img)
print "Conversion complete"


lisImages = filter((lambda x: x.endswith('.tif')), os.listdir(imageDir))
lisImages.sort()



'''Splits rasters into tiles and stores results in temporary folders'''
print "Creating subsets of time-series"

for num in range(len(lisImages)):
    
    dateString = lisImages[num].split(".")[3]                                               # Parse the date from the file name
    lisDates.append(int(dateString[4:7]))                                                   # Add the image date to the list of dates (lisDates)
    
    splitDir = os.path.join(tmpDir, str(num))                                               # Directory for storing split outputs
    os.mkdir(splitDir)                                                                      # Create folder for storing split outputs
    splitImg = os.path.join(imageDir, lisImages[num])                                       # Path to image that will be split
    arcpy.SplitRaster_management(splitImg,                                                  # SplitRaster function which outputs 4000 by
                                 splitDir, 
                                 "{0}.".format(lisImages[num][:len(lisImages[num])-4]), 
                                 "SIZE_OF_TILE", "TIFF", "", "", "4000 4000")
print "Subsetting complete"
 
splitLen = filter((lambda x: x.endswith('.TIF')), os.listdir(os.path.join(tmpDir, '0')))    # Make dynamic from splitdirs
splitDirs = filter((lambda x: type(int(x)) == int), os.listdir(tmpDir))
 
 
  
'''Check if temporary output directory exists and create one if not'''
if (os.path.exists(tmpoutDir)):
    next
else:
    os.mkdir(tmpoutDir)
      
       
'''Folders of split results'''
os.mkdir(os.path.join(tmpoutDir, 'SOS_Day'))
os.mkdir(os.path.join(tmpoutDir, 'EOS_Day'))
os.mkdir(os.path.join(tmpoutDir, 'SOS_NDVI'))
os.mkdir(os.path.join(tmpoutDir, 'EOS_NDVI'))
os.mkdir(os.path.join(tmpoutDir, 'MAX_Day'))
os.mkdir(os.path.join(tmpoutDir, 'MAX_NDVI'))
os.mkdir(os.path.join(tmpoutDir, 'SEAS_Duration'))
os.mkdir(os.path.join(tmpoutDir, 'SEAS_Amplitude'))
os.mkdir(os.path.join(tmpoutDir, 'SEAS_Integrated'))
os.mkdir(os.path.join(tmpoutDir, 'SEAS_PASG'))
  
  
  
for num in range(len(splitLen)):
    print "Processing subset {0}".format(num + 1)
     
    '''Image constants'''
    tmpImg = arcpy.Raster(os.path.join(tmpDir, splitDirs[0], splitLen[num]))                # Loads a temporary image to get metadata from
    imageWidth = tmpImg.width                                                               # Width of images in series
    imageHeight = tmpImg.height                                                             # Height of images in series
         
    dsc=arcpy.Describe(tmpImg)                                                              # Fetch metadata from temporary image
    arcpy.env.outputCoordinateSystem=dsc.SpatialReference                                   # Fetch coordinate system from metadata
         
    rasterExtentX = tmpImg.extent.XMin                                                      # Horizontal extent of series
    rasterExtentY = tmpImg.extent.YMin                                                      # Vertical extent of series
         
    rasterXCellSize = tmpImg.meanCellWidth                                                  # Mean width of series
    rasterYCellSize = tmpImg.meanCellHeight                                                 # Mean height of series
    tmpImg = None                                                                           # Clears raster from memory
         
                                                                                               
    '''Create numpy array to contain loaded timestack'''  
    imgStack = np.empty((imageHeight, imageWidth, len(splitDirs)), np.dtype('int16'))       # 3-D array that contains all of the images
                                                                                            # in a timeseries in 16-bit integer format
                                                                                               
    '''Creates arrays to contain results'''                                                                                        
    sosdayRaster = np.zeros((imageHeight, imageWidth), np.dtype('int16'))                   # Array that contains start of season days
    eosdayRaster = np.zeros((imageHeight, imageWidth), np.dtype('int16'))                   # Array that contains end of season days
    sosndviRaster = np.zeros((imageHeight, imageWidth), np.dtype('float32'))                # Array that contains start of season NDVI
    eosndviRaster = np.zeros((imageHeight, imageWidth), np.dtype('float32'))                # Array that contains end of season NDVI
    maxdayRaster = np.zeros((imageHeight, imageWidth), np.dtype('int16'))                   # Array that contains maximum NDVI day
    maxndviRaster = np.zeros((imageHeight, imageWidth), np.dtype('float32'))                # Array that contains maximum NDVI
    seasdurRaster = np.zeros((imageHeight, imageWidth), np.dtype('int16'))                  # Array that contains the season duration
    seasampRaster = np.zeros((imageHeight, imageWidth), np.dtype('float32'))                # Array that contains the season NDVI amplitude
    seasintegRaster = np.zeros((imageHeight, imageWidth), np.dtype('float32'))              # Array that contains time integrated NDVI
    seaspasgRaster = np.zeros((imageHeight, imageWidth), np.dtype('float32'))               # Array that contains percent average greeness
       
    lisDates = []                                                                           # List that contains the dates of the images
                                                                                            # in the series
                                                                                               
    '''Load the timeseries images into the timeseries array'''  
    startTime = time.time()
    for i, dir in enumerate(splitDirs):
        img = filter((lambda x: x.endswith('.TIF')),                                        # Current raster that will be loaded
                     os.listdir(os.path.join(tmpDir, dir)))[num]
        dateString = img.split(".")[3]                                                      # Parse the date from the file name
        lisDates.append(int(dateString[4:7]))                                               # Add the image date to the list of dates (lisDates)
                                             
    #     # Max NDVI !! Will need to loop through series !!
        imgStack[:, :, i] = arcpy.RasterToNumPyArray(os.path.join(tmpDir, dir, img),        # RasterToNumPyArray function converts raster 
                                                     arcpy.Point(rasterExtentX,             # into an array and loads it into the timeseries
                                                                 rasterExtentY),            # array (imgStack)
                                                     "", "", -9999)
         
    imgStack[:, :][imgStack[:, :]< 0] = 0                                                   # Changes all NDVI values that are below zero to zero
    endTime = time.time()
    print "Took {0} to load images".format(endTime - startTime)
   
    sortDates = np.array(lisDates)                                                          # Converts the list of dates (lisDates) into an
                                                                                            # array to make it compatible with curve fitting
       
    '''Initialize constants'''                                                                                        
    maxDay = 0
    maxNDVI = 0
    sosNDVI = 0
    sosDay = 0
         
    '''Gaussian function used to perform a Gaussian fit'''  
    def func_gauss(x, *p):
        A, mu, sigma = p                                                                    # Paramaters for the fit
        return A * np.exp(-(x-mu)**2/(2.*sigma**2))                                         # Calculation used to determine the fitted Y-value
       
    '''Inverted Gaussian function to determine X-values'''  
    def findX_gauss(y, *p):
        A, mu, sigma = p                                                                    # Paramaters for the fit
        return (-1 * math.sqrt((-1 * math.log(y/A)) * (2 * sigma**2))) + mu                 # Calculation used to determine the fitted X-value
    
         
    def dbl_logistic_model (p, agdd):
        return p[0] + p[1]* ( 1./(1+np.exp(p[2]*(agdd-p[3]))) + \
                              1./(1+np.exp(-p[4]*(agdd-p[5])))  - 1 )
         
    def findIndex(lst, val):
        return min(enumerate(lst), key=lambda x: abs(x[1]-val))[0]
    
    '''Curve fitting constants'''     
    popt = np.empty((3))
    p0 = [.7869, 202., 39.0803]                                                             # Parameters for Gaussian fit
    p1 = [0.8491, 0.9340, 0.6787, 90, 0.7431, 200]                                          # Parameters for Double Logistic fit
    newX = np.linspace(sortDates[0], sortDates[-1], (sortDates[-1] - sortDates[0]) + 1)     # Array that contains interpolated dates      
    count = 0
       
       
    '''Iterate through every pixel and perform fits'''
    for x in range(imageHeight):
        for y in range(imageWidth):
            lai = imgStack[x, y]                                                            # List of raw NDVI vales
               
            if (lai.all() == 0):
                pass
               
            filtY = np.where(lai == 0)[0]                                                   # Finds indexes of pixels that are outliers (<=0)
            lai = np.delete(lai, filtY, 0)                                                  # Deletes the outlier Y-values
            newdate = np.delete(sortDates, filtY, 0)                                         # Deletes the outlier X-values
                 
            try:
                popt, pcov = curve_fit(func_gauss, newdate, lai, p0)                        # Applies SciPy curve fit to the values and fetches
                                                                                            # fitting values (popt)              
                yFit = func_gauss(newX, *popt)                                              # Fits the raw Y-values using fitted values (popt)
                maxDay = popt[1]                                                            # Fetches the maximum NDVI day
                maxNDVI = popt[0]                                                           # Fetches the maximum NDVI
                sosNDVI = yFit[0] + ((maxNDVI - yFit[0]) * sosConst)                        # Determines that start of season NDVI
                sosDay = findX_gauss(sosNDVI, *popt)                                        # Determines the start of season day
                sosIndex = int(findIndex(newX, sosDay))
                eosNDVI = yFit[-1] + ((maxNDVI - yFit[-1]) * eosConst)                      # Determines the end of season NDVI
                
                eosDay = maxDay + (maxDay - findX_gauss(eosNDVI, *popt))#newX[eosIndex]     # Determines the end of season day    
                eosIndex = int(findIndex(newX, eosDay))                                               
                seasDur = eosDay - sosDay                                                   # Determines the duration of season
                seasAmp = maxNDVI - sosNDVI                                                 # Determines the NDVI amplitude
                seasInteg = np.trapz(yFit[sosIndex:eosIndex], newX[sosIndex:eosIndex])      # Determines the time integrated NDVI
                seasPASG = sum(yFit[sosIndex:eosIndex] - sosNDVI)                           # Determines the percent annual seasonal greeness
                 
                   
                '''Store results at the current pixel in the result rasters 
                 
                   Some results are divided by 10000 since the original NDVI
                   values were factored up by 10000 to fit into Int16 arrays
                '''
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


#                 plt.figure()
#                 plt.plot(newX, yFit, 'g-',ls='none', marker = '*',label="EXP")
#                 plt.plot(np.array(sosDay), np.array(sosNDVI), 'y-', ls = 'none', marker = 'D')
#                 plt.plot(np.array(eosDay), np.array(eosNDVI), 'y-', ls = 'none', marker = 'D')
#                 plt.show()
                
            except RuntimeError:
                pass
                           
            except TypeError:
                pass
                                                           
         
    '''Filter the data to remove error values'''
    sosdayRaster[(sosdayRaster < 0) | (sosdayRaster > 365)] = 0
    eosdayRaster[(eosdayRaster < 0) | (eosdayRaster > 365)] = 0
    sosndviRaster[(sosndviRaster < 0) | (sosndviRaster > 1)] = 0
    eosndviRaster[(eosndviRaster < 0) | (eosndviRaster > 1)] = 0
    maxdayRaster[(maxdayRaster < 0) | (maxdayRaster > 365)] = 0
    maxndviRaster[(maxndviRaster < 0) | (maxndviRaster > 1)] = 0
    seasdurRaster[(seasdurRaster < 0) | (seasdurRaster > 365)] = 0
    seasampRaster[(seasampRaster < 0) | (seasampRaster > 1)] = 0
    seaspasgRaster[(seaspasgRaster < 0) | (seaspasgRaster > 100)] = 0
       
     
    '''Convert the output arrays to rasters and save them in an output folder'''
    print "Exporting results to raster format"
                
    arcpy.NumPyArrayToRaster(sosdayRaster, arcpy.Point(rasterExtentX,             # into an array and loads it into the timeseries
                                                                 rasterExtentY), "", "", 0).save(os.path.join(tmpoutDir, "SOS_Day", "SOS_Day{0}.tif".format(num)))
    arcpy.NumPyArrayToRaster(eosdayRaster, arcpy.Point(rasterExtentX,             # into an array and loads it into the timeseries
                                                                 rasterExtentY), "", "", 0).save(os.path.join(tmpoutDir, "EOS_Day", "EOS_Day{0}.tif".format(num)))
    arcpy.NumPyArrayToRaster(sosndviRaster, arcpy.Point(rasterExtentX,             # into an array and loads it into the timeseries
                                                                 rasterExtentY), "", "", 0).save(os.path.join(tmpoutDir, "SOS_NDVI", "SOS_NDVI{0}.tif".format(num)))
    arcpy.NumPyArrayToRaster(eosndviRaster, arcpy.Point(rasterExtentX,             # into an array and loads it into the timeseries
                                                                 rasterExtentY), "", "", 0).save(os.path.join(tmpoutDir, "EOS_NDVI", "EOS_NDVI{0}.tif".format(num)))
    arcpy.NumPyArrayToRaster(maxdayRaster, arcpy.Point(rasterExtentX,             # into an array and loads it into the timeseries
                                                                 rasterExtentY), "", "", 0).save(os.path.join(tmpoutDir, "MAX_Day", "MAX_Day{0}.tif".format(num)))
    arcpy.NumPyArrayToRaster(maxndviRaster, arcpy.Point(rasterExtentX,             # into an array and loads it into the timeseries
                                                                 rasterExtentY), "", "", 0).save(os.path.join(tmpoutDir, "MAX_NDVI", "MAX_NDVI{0}.tif".format(num)))
    arcpy.NumPyArrayToRaster(seasdurRaster, arcpy.Point(rasterExtentX,             # into an array and loads it into the timeseries
                                                                 rasterExtentY), "", "", 0).save(os.path.join(tmpoutDir, "SEAS_Duration", "SEAS_Duration{0}.tif".format(num)))
    arcpy.NumPyArrayToRaster(seasampRaster, arcpy.Point(rasterExtentX,             # into an array and loads it into the timeseries
                                                                 rasterExtentY), "", "", 0).save(os.path.join(tmpoutDir, "SEAS_Amplitude", "SEAS_Amplitude{0}.tif".format(num)))
    arcpy.NumPyArrayToRaster(seasintegRaster, arcpy.Point(rasterExtentX,             # into an array and loads it into the timeseries
                                                                 rasterExtentY), "", "", 0).save(os.path.join(tmpoutDir, "SEAS_Integrated", "SEAS_Integrated{0}.tif".format(num)))
    arcpy.NumPyArrayToRaster(seaspasgRaster, arcpy.Point(rasterExtentX,             # into an array and loads it into the timeseries
                                                                 rasterExtentY), "", "", 0).save(os.path.join(tmpoutDir, "SEAS_PASG", "SEAS_PASG{0}.tif".format(num)))
    print "Exporting results to raster complete"     
         
    finalTime = time.time()
    print "Image took {0} minutes to process and finished at {1}".format(((finalTime - startTime) / 60), time.ctime())
    print num   
 
 
'''Mosaic the subsets and save the output raster in the output folder'''
print "Mosaicing subsets"

for subDir in os.listdir(tmpoutDir):
    intFolders = ["EOS_Day", "SOS_Day", "MAX_Day", "SEAS_Duration"]
    rasterDtype = None
     
    subRasters = filter((lambda x: x.endswith('.tif')), os.listdir(os.path.join(tmpoutDir, subDir)))
    saveName = "{0}.tif".format(subDir)
    arcpy.env.workspace = os.path.join(tmpoutDir, subDir)
     
    if (intFolders.count(subDir) > 0):
        rasterDtype = "16_BIT_UNSIGNED"
    else:
        rasterDtype = "32_BIT_FLOAT"
         
    arcpy.MosaicToNewRaster_management(subRasters, outDir, saveName, "",\
                                       rasterDtype, "", "1", "LAST","FIRST")
    
print "Process completed at {0}".format(time.ctime())
     
    
