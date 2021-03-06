
''' Imports '''
import arcpy
from arcpy import sa as arcsa
import os

arcpy.CheckOutExtension("Spatial")                                                      # Verifies that the Spatial Analyst extension is activated


# inputDir = r"I:\Scripts\GIS\YieldRow_Script\Test"
# rasterDir = os.path.join(inputDir, "rasters")

''' Directories '''
inputDir = arcpy.GetParameterAsText(0)                                                  # Directory that contains the ASCII files
rasterDir = arcpy.GetParameterAsText(1)                                                 # Directory that will contain the output rasters


''' Constants '''
ascFiles = filter((lambda x: x.endswith(".asc") and                                     # List of all the ASCII files in the input director
                   not("sd" in x)), os.listdir(inputDir))                               # NOTE: Filters out ASCII files that contain "sd" in them

convrasPaths = []                                                                       # List that stores the file paths to the converted ASCII rasters
totalRasters = len(ascFiles)                                                            # Calculates the number of ASCII input files
coordSys = "PROJCS['NAD_1983_UTM_Zone_17N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-81.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
finalRaster = os.path.join(rasterDir, "yi{0}year".format(totalRasters))
# os.mkdir(rasterDir)


for ascii in ascFiles:
    inputAscii = os.path.join(inputDir, ascii)
    rasterName = "{0}map".format(ascii.replace(".asc", ""))
    outputRaster = os.path.join(rasterDir, rasterName)
    convrasPaths.append(outputRaster)
    arcpy.ASCIIToRaster_conversion(inputAscii, outputRaster, "FLOAT")
    
meanRaster = arcsa.CellStatistics(convrasPaths, "MEAN", "DATA")
stdRaster = arcsa.CellStatistics(convrasPaths, "STD", "DATA")

arcsa.Divide(meanRaster, stdRaster).save(finalRaster)
arcpy.DefineProjection_management(finalRaster, coordSys)