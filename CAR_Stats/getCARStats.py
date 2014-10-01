import arcpy
import arcpy.sa as arcsa
import os

arcpy.CheckOutExtension('Spatial')
arcpy.env.overwriteOutput = True

mainDir = os.getcwd()
imgDir = os.path.join(mainDir, "image")
maskDir = os.path.join(mainDir, "masks")
carDir = os.path.join(mainDir, "car")
tmpDir = os.path.join(mainDir, "temp")

imgPath = os.path.join(imgDir, filter((lambda x: x.endswith('.tif')), os.listdir(imgDir))[0])
maskPath = os.path.join(maskDir, filter((lambda x: x.endswith('.tif')), os.listdir(maskDir))[0])
carPath = os.path.join(carDir, filter((lambda x: x.endswith('.shp')), os.listdir(carDir))[0])

joinFields = ['COUNT', 'AREA', 'MIN', 'MAX', 'RANGE', 'MEAN', 'STD', 'SUM']
delFields = ['ZONE_CODE', 'AREA', 'MEAN']

weekNum = 30
yearNum = 2014

modisProj = "PROJCS['User_Defined_Sinusoidal',GEOGCS['GCS_User_Defined',DATUM['D_User_Defined',SPHEROID['User_Defined_Spheroid',6371007.181,0.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Sinusoidal'],PARAMETER['false_easting',0.0],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',0.0],UNIT['Meter',1.0]]"
maskProj = "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],METADATA['North America - NAD83',167.65,14.93,-47.74,86.45,0.0,0.0174532925199433,0.0,1350]]"

arcpy.CreateCustomGeoTransformation_management("NAD83_to_MODIS_SPHERE", maskProj, modisProj, "GEOGTRAN[METHOD['Longitude_Rotation']]")
arcpy.ProjectRaster_management(maskPath, os.path.join(tmpDir, "project_mask.tif"), imgPath, "", "", "NAD1983_TO_MODIS_SPHERE")
print "Finished projection"
arcsa.Times(imgPath, maskPath).save(os.path.join(tmpDir, "masked.tif"))
print "Finished times"
arcsa.ZonalStatisticsAsTable(carPath, 'CARUID', os.path.join(tmpDir, "masked.tif"), os.path.join(tmpDir, "table.dbf"), 'DATA', 'ALL')
 
 
#arcsa.ZonalStatisticsAsTable(carPath, 'CARUID', maskPath, os.path.join(tmpDir, "table"), 'DATA', 'ALL')
 
maskedRaster = arcpy.Raster(os.path.join(tmpDir, "masked.tif"))
arcsa.Con(arcsa.IsNull(maskedRaster), 0, maskedRaster).save(os.path.join(tmpDir, "rastercalc.tif"))
arcsa.ZonalStatisticsAsTable(carPath, 'CARUID', os.path.join(tmpDir, "project_mask.tif"), os.path.join(tmpDir, "test.dbf"), 'DATA', 'MEAN')
arcpy.DeleteField_management(os.path.join(tmpDir, "test.dbf"), delFields)
 
 
arcpy.JoinField_management(os.path.join(tmpDir, "test.dbf"), 'CARUID', os.path.join(tmpDir, "table.dbf"), 'CARUID', joinFields)
arcpy.AddField_management(os.path.join(tmpDir, "test.dbf"), 'YEAR', 'SHORT')
arcpy.AddField_management(os.path.join(tmpDir, "test.dbf"), 'WEEK', 'SHORT')
arcpy.CalculateField_management(os.path.join(tmpDir, "test.dbf"), 'YEAR', yearNum, 'PYTHON')
arcpy.CalculateField_management(os.path.join(tmpDir, "test.dbf"), 'WEEK', weekNum, 'PYTHON')





































# try:
#     os.mkdir(os.path.join(carDir, "split_CAR"))
#     carSplit = os.path.join(carDir, "split_CAR")
# except OSError:
#     shutil.rmtree(os.path.join(carDir, "split_CAR"))
#     os.mkdir(os.path.join(carDir, "split_CAR"))
#     carSplit = os.path.join(carDir, "split_CAR")
#     
# try:
#     os.mkdir(os.path.join(maskDir, "clip_mask"))
#     maskClip = os.path.join(maskDir, "clip_mask")
# except OSError:
#     shutil.rmtree(os.path.join(maskDir, "clip_mask"))
#     os.mkdir(os.path.join(maskDir, "clip_mask"))
#     maskClip = os.path.join(maskDir, "clip_mask")
#     
# try:
#     os.mkdir(os.path.join(imgDir, "clip_image"))
#     imageClip = os.path.join(imgDir, "clip_image")
# except OSError:
#     shutil.rmtree(os.path.join(imgDir, "clip_image"))
#     os.mkdir(os.path.join(imgDir, "clip_image"))
#     imageClip = os.path.join(imgDir, "clip_image")
#     
# try:
#     os.mkdir(os.path.join(mainDir, 'temp'))
#     tmpDir = os.path.join(mainDir, 'temp')
# except OSError:
#     shutil.rmtree(os.path.join(mainDir, 'temp'))
#     os.mkdir(os.path.join(mainDir, 'temp'))
#     tmpDir = os.path.join(mainDir, 'temp')
#     
# arcpy.Split_analysis(carPath, carPath, 'CARUID', carSplit)
# 
# clipLst = filter((lambda x: x.endswith('.shp')), os.listdir(carSplit))
# 
# for clip in clipLst:
#     imgExtract = arcsa.ExtractByMask(imgPath, os.path.join(carSplit, clip))
#     imgExtract.save(os.path.join(imageClip, '{0}_image.tif'.format(clip)))
#     mskExtract = arcsa.ExtractByMask(maskPath, os.path.join(carSplit, clip))
#     imgExtract.save(os.path.join(maskClip, '{0}_mask.tif'.format(clip)))
#     
#     mskImage = arcsa.Times(os.path.join(imageClip, '{0}_image.tif'.format(clip)), os.path.join(maskClip, '{0}_mask.tif'.format(clip)))
#     mskImage.save(os.path.join(tmpDir, '{0}_masked.tif'.format(clip)))
#         
