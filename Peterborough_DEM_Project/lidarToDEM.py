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
comparedemIn = arcpy.GetParameterAsText(5)
coordsysIn = arcpy.GetParameterAsText(6)

lasLst = []                 # List of all of the las files in index
lasdOut = os.path.join(outDir, "tiled_LAS.lasd")
demOut = os.path.join(outDir, "DEM.tif")
groundpolyOut = os.path.join(outDir, "Ground_Polygon.shp")
nongroundpolyOut = os.path.join(outDir, "Non_Ground_Polygon.shp")
minusrasOut = os.path.join(outDir, "Minus_Raster.tif")
groundrasOut = os.path.join(outDir, "Ground_Raster.tif")
nongroundrasOut = os.path.join(outDir, "Non_Ground_Raster.tif")

arcpy.MakeFeatureLayer_management(lidartileIn, "LAS_Index")
 
with arcpy.da.SearchCursor("LAS_Index", ["FID", tileField]) as cursor:                  # @UndefinedVariable
    for row in cursor:
        if (arcpy.Exists(os.path.join(lidarIn, row[1] + ".las"))):
            lasLst.append(os.path.join(lidarIn, row[1] + ".las"))
        else: pass
     
arcpy.CreateLasDataset_management(lasLst, lasdOut, "NO_RECURSION", "", coordsysIn)
arcpy.LasDatasetToRaster_conversion(lasdOut, demOut, "ELEVATION", "BINNING MINIMUM SIMPLE", "FLOAT", "CELLSIZE", cellSize, "1")

arcpy.Minus_3d(demOut, comparedemIn, minusrasOut)
arcpy.gp.Con_sa(minusrasOut, "1", groundrasOut, "", "Value < .5")
arcpy.RasterToPolygon_conversion(groundrasOut, groundpolyOut, "NO_SIMPLIFY", "VALUE")
# arcpy.Delete_management("in_memory\\ground")

arcpy.gp.Con_sa(minusrasOut, "1", nongroundrasOut, "", "Value > .5")
# arcpy.Delete_management("in_memory\\diff")
arcpy.RasterToPolygon_conversion(nongroundrasOut, nongroundpolyOut, "NO_SIMPLIFY", "VALUE")



                           
    


