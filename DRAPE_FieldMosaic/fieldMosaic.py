import arcpy, os, shutil
from arcpy import sa as arcsa

arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

rastersIn = arcpy.GetParameterAsText(0)
agrishpIn = arcpy.GetParameterAsText(1)
outDir = arcpy.GetParameterAsText(2)
numBands = arcpy.GetParameterAsText(3)


workDir = os.path.join(outDir, "temp")
yearshpDir = os.path.join(workDir, "year_shapefiles")
cliprasterDir = os.path.join(workDir, "clipped_rasters")

rasterLst = rastersIn.split(';')
yearsLst = []
rasterDict = {}
agrishpDict = {}
cliprastDict = {}
 

for raster in rasterLst:
    rastYear = raster.split('\\')[-1].split('_')[0]
    yearsLst.append(rastYear)
    rasterDict[rastYear] = raster
    agrishpDict[rastYear] = os.path.join(yearshpDir, "{0}_data.shp".format(rastYear))
    cliprastDict[rastYear] = os.path.join(cliprasterDir, "{0}_raster.tif".format(rastYear))
 
if (os.path.exists(workDir)):
    shutil.rmtree(workDir, True)
    shutil.rmtree(yearshpDir, True)
    shutil.rmtree(cliprasterDir, True)
    
os.mkdir(workDir)
os.mkdir(yearshpDir)
os.mkdir(cliprasterDir)

for year in yearsLst:
    if (year is max(yearsLst)):
        arcpy.AddMessage("{0}, {1}".format(agrishpIn, agrishpDict[year]))
        arcpy.FeatureClassToFeatureClass_conversion(agrishpIn, yearshpDir, "{0}_data.shp".format(year), "YEAR = {0} OR YEAR = 0".format(year))
        arcsa.ExtractByMask(rasterDict[year], agrishpDict[year]).save(cliprastDict[year])
        arcpy.SetRasterProperties_management(cliprastDict[year],nodata="1 0;2 0;3 0")
    else:
        arcpy.AddMessage("{0}, {1}, {2}".format(agrishpIn, agrishpDict[year], year))
        arcpy.FeatureClassToFeatureClass_conversion(agrishpIn, yearshpDir, "{0}_data.shp".format(year), "YEAR = {0}".format(year))
        arcsa.ExtractByMask(rasterDict[year], agrishpDict[year]).save(cliprastDict[year])
        arcpy.SetRasterProperties_management(cliprastDict[year],nodata="1 0;2 0;3 0")
 
 
for year in yearsLst:
    if (arcpy.Describe(cliprastDict[year]).bandCount != numBands):
        arcpy.CompositeBands_management("{0}\\Band_1;{0}\\Band_2;{0}\\Band_3".format(cliprastDict[year]), cliprastDict[year])

        