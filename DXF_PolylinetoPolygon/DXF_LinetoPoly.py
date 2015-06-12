import arcpy
import os



inputDir = arcpy.GetParameterAsText(0)
workDir = arcpy.GetParameterAsText(1)
outputDir = arcpy.GetParameterAsText(2)
aggregDist = arcpy.GetParameterAsText(3)
bufferDist = arcpy.GetParameterAsText(4)

NAD83Proj = 'GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433],AUTHORITY["EPSG",4269]]'
lambProj = 'PROJCS["MNR_Lambert_Conformal_Conic",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",930000.0],PARAMETER["False_Northing",6430000.0],PARAMETER["Central_Meridian",-85.0],PARAMETER["Standard_Parallel_1",44.5],PARAMETER["Standard_Parallel_2",53.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'

dxfLst = filter(lambda x: x.endswith('.dxf'), os.listdir(inputDir))

for dxf in dxfLst:
    dxfPath = os.path.join(inputDir, dxf, 'Polyline')
    linePath = os.path.join(workDir, '{0}.shp'.format(dxf[:len(dxf) - 4]))
    projectPath = os.path.join(workDir, "projected.shp")
    bufferPath = os.path.join(workDir, "buffer.shp")
    finalPath = os.path.join(outputDir, '{0}_border.shp'.format(dxf[:len(dxf) - 4]))
    
    
    
    # arcpy.CopyFeatures_management(inputDir, inputlinePath)
    arcpy.FeatureClassToFeatureClass_conversion(dxfPath, workDir, dxf[:len(dxf) - 4])
    arcpy.DefineProjection_management(linePath, NAD83Proj)
    arcpy.Project_management(linePath, projectPath, lambProj)
    arcpy.Buffer_analysis(projectPath, bufferPath, bufferDist)
    arcpy.AggregatePolygons_cartography(bufferPath, finalPath, aggregDist, "", "", "ORTHOGONAL")
