import arcpy, os
from arcpy import sa as arcsa

arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
arcpy.CheckExtension("3D")

''' User inputs'''
lidarIn = arcpy.GetParameterAsText(0)                                                   # Directory that contains the .las files
lidartileIn = arcpy.GetParameterAsText(1)                                               # Shapefile that contains the tile index fields
tileField = arcpy.GetParameterAsText(2)                                                 # Field that contains the tile values or labels
outDir = arcpy.GetParameterAsText(3)                                                    # Output directory for the final DEM
cellSize = arcpy.GetParameterAsText(4)                                                  # Cell size for the output of the DEM
coordsysIn = arcpy.GetParameterAsText(5)                                                # Coordinate system for the LAS dataset and DEM raster


'''Constants'''
lasLst = []                                                                             # List of all of the las files in index
lasdOut = os.path.join(outDir, "tiled_LASD.lasd")                                       # Path for LASD containing all of the point cloud classes
belasdOut = os.path.join(outDir, "ground_LASD")                                         # Path for Filtered LASD that contains only ground points
demOut = os.path.join(outDir, "DTM.tif")                                                # Path for the final output DEM

           

arcpy.MakeFeatureLayer_management(lidartileIn, "LAS_Index")
 
with arcpy.da.SearchCursor("LAS_Index", ["FID", tileField]) as cursor:                  # @UndefinedVariable
    for row in cursor:
        if (arcpy.Exists(os.path.join(lidarIn, row[1] + ".las"))):
            lasLst.append(os.path.join(lidarIn, row[1] + ".las"))
        else:
            pass

arcpy.AddMessage("Creating LAS Dataset")     
arcpy.CreateLasDataset_management(lasLst, lasdOut, "NO_RECURSION", "", coordsysIn)
 
arcpy.AddMessage("Filtering LAS Dataset Points")
arcpy.MakeLasDatasetLayer_management(lasdOut, belasdOut, [2])
 
arcpy.AddMessage("Converting LAS Dataset to Raster")
arcpy.LasDatasetToRaster_conversion(belasdOut, demOut, "ELEVATION", "BINNING NEAREST NATURAL_NEIGHBOR", "FLOAT", "CELLSIZE", cellSize, "1")



                           
    


