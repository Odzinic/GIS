import numpy
import arcpy

img = r'E:\GIS\Work\EOS_day.tif' # Path

raster = arcpy.Raster(img)
rasArray = arcpy.RasterToNumPyArray(raster)

print rasArray