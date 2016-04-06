import os
import arcpy

# Input shapefiles to be compared
# liosoilInput = r"J:\Scripts\GIS\LIO_SoilCompare\LIO-2014-06-20\LIOEditor_SoilSurveyComplex_March42015.shp"
# publicsoilInput = r"J:\Scripts\GIS\LIO_SoilCompare\LIO-2014-06-20\SOIL_SURVEY_COMPLEX.shp"

liosoilInput = r"J:\Scripts\GIS\LIO_SoilCompare\LIO-2014-06-20\LIOEditor_Point.shp"
publicsoilInput = r"J:\Scripts\GIS\LIO_SoilCompare\LIO-2014-06-20\SOIL_SURVEY_POINT.shp"
# Output folder
outDir = r"J:\Scripts\GIS\LIO_SoilCompare\output"

# Output File Paths
diffLayer = os.path.join(outDir, "poly_diff.shp")                                           # Output shapefile that displays polygon differences
                                                                                            # between the two shapefiles
resultDb = os.path.join(outDir, "results.gdb")                                              # Geodatabase that is used to store the comparison table
compareTxt = os.path.join(outDir, "Compare_Results.txt")                                    # Text file that contains the differences between the two
                                                                                            # shapefiles
compareTbl = os.path.join(resultDb, "Compare_Results")                                      # The comparison text file loaded into the geodatabase to
                                                                                            # allow for easier creation of relates or joins


# Layers
in1 = arcpy.mapping.Layer(liosoilInput)                                                     # LIO shapefile loaded as a layer to allow for location and
                                                                                            # attribute queries
in2 = arcpy.mapping.Layer(publicsoilInput)                                                  # Public shapefile loaded as a layer to allow for location and
                                                                                            # attribute queries
                                                                                            
countDict = {}


# Parameters for arcpy Feature Compare tool
ignOptions = 'IGNORE_M;IGNORE_Z;IGNORE_POINTID;IGNORE_EXTENSION_PROPERTIES;IGNORE_SUBTYPES;IGNORE_RELATIONSHIPCLASSES;\
IGNORE_REPRESENTATIONCLASSES'
omitOptions = "FID;Shape;OGF_ID;MAPUNIT;ACRES;HECTARES;ACCURACY;GEO_UPT_DT;EFF_DATE"


lioFields = arcpy.ListFields(liosoilInput)
keepFields = ["Message", "OBJECTID"]

if (not arcpy.Exists(resultDb)):
    arcpy.CreateFileGDB_management(outDir, "results.gdb")


with arcpy.da.SearchCursor(compareTbl, ['ObjectID_1']) as cursor:
    for row in cursor:
        if (countDict.has_key(row[0])):
            countDict[row[0]] += 1
        else:
            countDict[row[0]] = 1
            
with arcpy.da.UpdateCursor(publicsoilInput, ['FID', 'DIFF_FIELD']) as cursor:
    for row in cursor:
        try:
            row[1] = countDict[row[0]]
            cursor.updateRow(row)
        except KeyError:
            pass
        
        

