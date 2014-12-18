import arcpy
import arcpy.sa as arcsa
import os
from shutil import copyfile

arcpy.CheckOutExtension('Spatial')
arcpy.env.overwriteOutput = True
arcpy.env.pyramid = "None"

''' Directories '''
mainDir = os.getcwd()                                                                                       # Root folder of script                      
imgDir = os.path.join(mainDir, "image")                                                                     # Directory for MODIS image
maskDir = os.path.join(mainDir, "masks")                                                                    # Directory for crop mask
carDir = os.path.join(mainDir, "car")                                                                       # Directory for CAR shapefile
tmpDir = os.path.join(mainDir, "temp")                                                                      # Temporary directory
outDir = os.path.join(mainDir, "output")                                                                    # Output directory


'''Check if output directory exists and create one if not'''
if (os.path.exists(outDir)):
    next
else:
    os.mkdir(outDir)
    

''' Path constants '''
lisImages = filter((lambda x: x.endswith('.tif')), os.listdir(imgDir))                                      # List of  MODIS images
maskPath = os.path.join(maskDir, filter((lambda x: x.endswith('.tif')), os.listdir(maskDir))[0])            # Path to crop mask
carPath = os.path.join(carDir, filter((lambda x: x.endswith('.shp')), os.listdir(carDir))[0])               # Path to CAR shapefile
timesImg = os.path.join(tmpDir, "times_img.tif") 
projmaskPath = os.path.join(tmpDir, "project_mask.tif")                                                     # Path to projected mask
maskedPath = os.path.join(tmpDir, "masked.tif")                                                             # Path to masked MODIS image
statsTable = os.path.join(tmpDir, "statistics.dbf")
totcountTable = os.path.join(tmpDir, "total_count.dbf")


''' Projection constants '''
# Used to project the crop mask to the user defined
# sinusoidal projection of MODIS images
modisProj = "PROJCS['User_Defined_Sinusoidal',GEOGCS['GCS_User_Defined',DATUM['D_User_Defined',SPHEROID['User_Defined_Spheroid',6371007.181,0.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Sinusoidal'],PARAMETER['false_easting',0.0],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',0.0],UNIT['Meter',1.0]]"
maskProj = "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],METADATA['North America - NAD83',167.65,14.93,-47.74,86.45,0.0,0.0174532925199433,0.0,1350]]"


''' Constants '''
joinFields = ['COUNT', 'AREA', 'MIN', 'MAX', 'RANGE', 'MEAN', 'STD', 'SUM']                                 # Fields that will be kept from Zonal
                                                                                                            # statistics output of masked raster
delFields = ['ZONE_CODE', 'AREA', 'MEAN']                                                                   # Fields that will be deleted from Zonal
                                                                                                            # statistics output of crop mask

dayNum = 0                                                                                                  # Week number of MODIS image
yearNum = 0                                                                                                 # Year number of MODIS image


''' Projecting crop mask to MODIS coordinate system '''
 
arcpy.CreateCustomGeoTransformation_management("NAD83_to_MODIS_SPHERE", maskProj, modisProj, 
                                               "GEOGTRAN[METHOD['Longitude_Rotation']]")
arcpy.ProjectRaster_management(maskPath, projmaskPath, 
                               os.path.join(imgDir, lisImages[0]), "", "", "NAD1983_TO_MODIS_SPHERE")
 
print "Projecting completed"


for img in lisImages:
    imgPath = os.path.join(imgDir, img)
    
    ''' Applying crop mask to MODIS image '''
    arcsa.Times(imgPath, projmaskPath).save(timesImg)                                                       # Times function to set masked out pixels as 0
    arcsa.SetNull(timesImg, timesImg, "VALUE = 0").save(maskedPath)                                         # Sets all 0 values to NoData
 
    print "Masking completed"
 
 
    ''' Running zonal statistics on images '''
    # A table named statistics.dbf is created and contains
    # the statistics of the masked MODIS image, then another
    # table is named total_count.dbf created containing statistics of the crop mask
    # to allow for a comparison of pixel counts and includes
    # areas with NoData
    arcsa.ZonalStatisticsAsTable(carPath, 'CARUID', maskedPath, statsTable, 'DATA', 'ALL')                  # Zonal statistics of entire image      
    arcsa.ZonalStatisticsAsTable(carPath, 'CARUID', imgPath, totcountTable, 'DATA', 'MEAN')                 # Zonal statistics to find CAR count before masking
 
    print "Zonal statistics completed"
     

    ''' Finding date '''
    yearNum = int(img.split('.')[3][:4])                                                                    # Parses the name of the image using split and 
                                                                                                            # fetches the year                                                                 
    dayNum = int(img.split('.')[3][4:])                                                                     # Parses the name of the image using split and 
                                                                                                            # fetches the day


    ''' Joining tables together '''
    arcpy.DeleteField_management(totcountTable, delFields) 
    arcpy.JoinField_management(statsTable, 'CARUID', totcountTable, 'CARUID', joinFields)
    
    print "Joining tables completed"
    
    
    '''Adding year and date information to the table'''
    arcpy.AddField_management(statsTable, 'YEAR', 'SHORT')
    arcpy.AddField_management(statsTable, 'DAY', 'SHORT')
    arcpy.CalculateField_management(statsTable, 'YEAR', yearNum, 'PYTHON')
    arcpy.CalculateField_management(statsTable, 'DAY', dayNum, 'PYTHON')

    
    '''Copy final table to output directory'''
    copyfile(statsTable, os.path.join(outDir, "{0}.dbf").format(img[:len(img)-4]))
    
    print "Table saved at {0}".format(os.path.join(outDir, "{0}.dbf"))
