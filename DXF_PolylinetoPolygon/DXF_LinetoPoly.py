import arcpy
import os

arcpy.env.overwriteOutput = True

# inputDir = arcpy.GetParameterAsText(0)
# workDir = arcpy.GetParameterAsText(1)
# outputDir = arcpy.GetParameterAsText(2)
# aggregDist = arcpy.GetParameterAsText(3)
# bufferDist = arcpy.GetParameterAsText(4)
# fileType = arcpy.GetParameterAsText(5)

inputDir = r"J:\Scripts\GIS\DXF_PolylinetoPolygon\input"
workDir = r"J:\Scripts\GIS\DXF_PolylinetoPolygon\New Folder"
outputDir = r"J:\Scripts\GIS\DXF_PolylinetoPolygon\out"
aggregDist = "25 Meters"
bufferDist = "10 Meters"
fileType = ".shp"

NAD83Proj = 'GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433],AUTHORITY["EPSG",4269]]'
lambProj = 'PROJCS["MNR_Lambert_Conformal_Conic",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",930000.0],PARAMETER["False_Northing",6430000.0],PARAMETER["Central_Meridian",-85.0],PARAMETER["Standard_Parallel_1",44.5],PARAMETER["Standard_Parallel_2",53.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
utm17Proj = 'PROJCS["NAD_1983_UTM_Zone_17N",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-81.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0],AUTHORITY["EPSG",26917]]'
utm18Proj = 'PROJCS["NAD_1983_UTM_Zone_18N",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-75.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0],AUTHORITY["EPSG",26918]]'
utm16Proj = 'PROJCS["NAD_1983_UTM_Zone_16N",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-87.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0],AUTHORITY["EPSG",26916]]'
projLst = [lambProj, utm17Proj, utm18Proj, utm16Proj]
projPos = 0

errorPath = os.path.join(outputDir, "error_log.txt")
errorLog = open(errorPath, 'w')

def findProjection(input, output, projs, pos, count):
    if (count > 3):
        return 0
    if (pos > 3):
        print "past 3"
        pos = 0
        
    try:
        arcpy.Project_management(input, output, projs[pos])
        return pos
        
    except arcpy.ExecuteError:
        print pos
        pos += 1
        count += 1
        return findProjection(input, output, projs, pos, count)

if ("dxf" in fileType):
    dxfLst = filter(lambda x: x.endswith('.dxf'), os.listdir(inputDir))
    for dxf in dxfLst:
        dxfPath = os.path.join(inputDir, dxf, 'Polyline')
        linePath = os.path.join(workDir, '{0}.shp'.format(dxf[:len(dxf) - 4]))
        projectPath = os.path.join(workDir, "projected.shp")
        bufferPath = os.path.join(workDir, "buffer.shp")
        finalPath = os.path.join(outputDir, '{0}_border.shp'.format(dxf[:len(dxf) - 4]))
             
        try:
            arcpy.FeatureClassToFeatureClass_conversion(dxfPath, workDir, dxf[:len(dxf) - 4])
            arcpy.DefineProjection_management(linePath, NAD83Proj)
#             arcpy.Project_management(linePath, projectPath, lambProj)
            projPos = findProjection(linePath, projectPath, projLst, projPos, 0)
            arcpy.Buffer_analysis(projectPath, bufferPath, bufferDist)
            arcpy.AggregatePolygons_cartography(bufferPath, finalPath, aggregDist, "", "", "ORTHOGONAL")
        except arcpy.ExecuteError:
            errorLog.write('Error projecting {0}\n'.format(dxfPath))
            pass
        
elif ("dwg" in fileType):
    dwgLst = filter(lambda x: x.endswith('.dwg'), os.listdir(inputDir))
    for dwg in dwgLst:
        dwgPath = os.path.join(inputDir, dwg, 'Polyline')
        linePath = os.path.join(workDir, '{0}.shp'.format(dwg[:len(dwg) - 4]))
        projectPath = os.path.join(workDir, "projected.shp")
        bufferPath = os.path.join(workDir, "buffer.shp")
        finalPath = os.path.join(outputDir, '{0}_border.shp'.format(dwg[:len(dwg) - 4]))
        
        
        try:
            arcpy.FeatureClassToFeatureClass_conversion(dwgPath, workDir, dwg[:len(dwg) - 4])
            arcpy.DefineProjection_management(linePath, NAD83Proj)
#             arcpy.Project_management(linePath, projectPath, lambProj)
            projPos = findProjection(linePath, projectPath, projLst, projPos, 0)
            arcpy.Buffer_analysis(projectPath, bufferPath, bufferDist)
            arcpy.AggregatePolygons_cartography(bufferPath, finalPath, aggregDist, "", "", "ORTHOGONAL")
        except arcpy.ExecuteError:
            errorLog.write('Error projecting {0}\n'.format(dwgPath))
            pass
        
elif ("shp" in fileType):
    shpLst = filter(lambda x: x.endswith('.shp'), os.listdir(inputDir))
    
    for shp in shpLst:
        shpPath = os.path.join(inputDir, shp)
        linePath = os.path.join(workDir, '{0}.shp'.format(shp[:len(shp) - 4]))
        projectPath = os.path.join(workDir, "projected.shp")
        bufferPath = os.path.join(workDir, "buffer.shp")
        finalPath = os.path.join(outputDir, '{0}_border.shp'.format(shp[:len(shp) - 4]))
        
        
        
        try:
            arcpy.FeatureClassToFeatureClass_conversion(shpPath, workDir, shp[:len(shp) - 4])
            arcpy.DefineProjection_management(linePath, NAD83Proj)
#             arcpy.Project_management(linePath, projectPath, lambProj)
            projPos = findProjection(linePath, projectPath, projLst, projPos, 0)
            arcpy.Buffer_analysis(projectPath, bufferPath, bufferDist)
            arcpy.AggregatePolygons_cartography(bufferPath, finalPath, aggregDist, "", "", "ORTHOGONAL")
        except arcpy.ExecuteError:
            errorLog.write('Error projecting {0}\n'.format(shpPath))
            pass
        

    
    
errorLog.close()
