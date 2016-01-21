import arcpy, os
from arcpy import sa as arcsa

arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
arcpy.CheckExtension("3D")


lidarIn = arcpy.GetParameterAsText(0)
lidartileIn = arcpy.GetParameterAsText(1)
tileField = arcpy.GetParameterAsText(2)
outDir = arcpy.GetParameterAsText(3)
cellSize = arcpy.GetParameterAsText(4)

lasLst = []                 # List of all of the las files in index
lasdOut = os.path.join(outDir, "tiled_LAS.lasd")
demOut = os.path.join(outDir, "DEM.tif")

arcpy.MakeFeatureLayer_management(lidartileIn, "LAS_Index")

with arcpy.da.SearchCursor("LAS_Index", ["FID", tileField]) as cursor:                  # @UndefinedVariable
    for row in cursor:
        lasLst.append(os.path.join(lidarIn, row[1] + ".las"))
    
arcpy.CreateLasDataset_management(lasLst, lasdOut, "NO_RECURSION")
arcpy.LasDatasetToRaster_conversion(lasdOut, demOut, "ELEVATION", "BINNING MINIMUM SIMPLE", "FLOAT", "CELLSIZE", cellSize, "1")
                           
    


