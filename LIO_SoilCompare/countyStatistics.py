import arcpy
from arcpy import env
import os

arcpy.env.overwriteOutput = True

outGDB = r"J:\Scripts\GIS\LIO_SoilCompare\test_gdb.gdb"

env.workspace = r"J:\Scripts\GIS\LIO_SoilCompare\Assessments.gdb"

fcList = arcpy.ListFeatureClasses('', '', 'ALL_COMPARE')

env.workspace = env.workspace = r"J:\Scripts\GIS\LIO_SoilCompare\Assessments.gdb\ALL_COMPARE"

for fc in fcList:
    fieldName = fc
    outPath = os.path.join(outGDB, "{0}_table".format(fc))
    arcpy.Statistics_analysis(fc, outPath, [[fc, "COUNT"]], "SURVEY1")
