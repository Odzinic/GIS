import os
import arcpy

# Input shapefiles to be compared
liosoilInput = r"J:\LIO_SoilSurveyComplex\LIO_Copy\LIOEditor_SoilSurveyComplex_March42015.shp"
publicsoilInput = r"J:\LIO_SoilSurveyComplex\Public_Copy\Soil_Survey_Complex.shp"

# Output folder
outDir = r"J:\LIO_SoilSurveyComplex\output"

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


# Parameters for arcpy Feature Compare tool
ignOptions = 'IGNORE_M;IGNORE_Z;IGNORE_POINTID;IGNORE_EXTENSION_PROPERTIES;IGNORE_SUBTYPES;IGNORE_RELATIONSHIPCLASSES;\
IGNORE_REPRESENTATIONCLASSES'
omitOptions = 'FID;Shape;OBJECTID;EDIT_STATE;OGF_ID;Shape_Leng;Area_Acres'


lioFields = arcpy.ListFields(liosoilInput)
keepFields = ["Message", "ObjectID_1", "OBJECTID"]

if (not arcpy.Exists(resultDb)):
    arcpy.CreateFileGDB_management(outDir, "results.gdb")

arcpy.SelectLayerByLocation_management(in1, "ARE_IDENTICAL_TO", in2)
arcpy.SelectLayerByAttribute_management(in1, "SWITCH_SELECTION")
arcpy.CopyFeatures_management(in1, diffLayer)
 
arcpy.FeatureCompare_management(liosoilInput, publicsoilInput, 'Compare', 'ATTRIBUTES_ONLY', ignOptions, "0.000000008983 Unknown", "0.001", "0.001", "", omitOptions, 'CONTINUE_COMPARE', compareTxt)
arcpy.TableToGeodatabase_conversion(compareTxt, resultDb)
removeFields = filter(lambda x: x.name not in keepFields, arcpy.ListFields(compareTbl))
for field in arcpy.ListFields(compareTbl):
    arcpy.AddMessage(field.name)
arcpy.AddMessage(removeFields)


for field in removeFields:
    arcpy.DeleteField_management(compareTbl, field.name)