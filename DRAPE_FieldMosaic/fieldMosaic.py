import arcpy, os
from arcpy import sa as arcsa

arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

raster2008In = arcpy.GetParameterAsText(0)
raster2011In = arcpy.GetParameterAsText(1)
raster2014In = arcpy.GetParameterAsText(2)
agrishpIn = arcpy.GetParameterAsText(3)
outDir = arcpy.GetParameterAsText(4)
numBands = arcpy.GetParameterAsText(5)

workDir = os.path.join(outDir, "temp")
yearshpDir = os.path.join(workDir, "year_shapefiles")
cliprasterDir = os.path.join(workDir, "clipped_rasters")

agri2008Shp = os.path.join(yearshpDir, "2008_data.shp")
agri2011Shp = os.path.join(yearshpDir, "2011_data.shp")
agri2014Shp = os.path.join(yearshpDir, "2014_data.shp")

clip2008Ras = os.path.join(cliprasterDir, "2008_raster.tif")
clip2011Ras = os.path.join(cliprasterDir, "2011_raster.tif")
clip2014Ras = os.path.join(cliprasterDir, "2014_raster.tif")

os.mkdir(workDir)
os.mkdir(yearshpDir)
os.mkdir(cliprasterDir)



arcpy.FeatureClassToFeatureClass_conversion(agrishpIn, yearshpDir, "2008_data.shp", "YEAR = 2008")
arcpy.FeatureClassToFeatureClass_conversion(agrishpIn, yearshpDir, "2011_data.shp", "YEAR = 2011")
arcpy.FeatureClassToFeatureClass_conversion(agrishpIn, yearshpDir, "2014_data.shp", "YEAR = 2014 OR YEAR = 0")

arcsa.ExtractByMask(raster2008In, agri2008Shp).save(clip2008Ras)
arcsa.ExtractByMask(raster2011In, agri2011Shp).save(clip2011Ras)
arcsa.ExtractByMask(raster2014In, agri2014Shp).save(clip2014Ras)

for raster in [clip2008Ras, clip2011Ras, clip2014Ras]:
    if (arcpy.Describe(raster).bandCount != numBands):
        arcpy.CompositeBands_management("{0}\\Band_1;{0}\\Band_2;{0}\\Band_3".format(raster), raster)

        