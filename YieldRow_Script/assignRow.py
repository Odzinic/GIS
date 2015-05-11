import os
import arcpy
from arcpy import sa as arcs
from arcpy import da as arcda #@UnresolvedImport
arcpy.CheckOutExtension('Spatial')                                                      # Verifies that the Spatial Analyst extension is activated

input_dir = os.path.join(os.getcwd(), "input")

inputs = os.listdir(input_dir)                                                            # List that loads all files in the mask/buffer directory
points = os.path.join(input_dir, filter((lambda x: x.endswith(".shp")), inputs)[0])       # Loads only shapefile masks/buffers to prevent useless files

currDegree = 0
prevDegree = 70
pathNum = 0
pathList = []
pathLen = {}
threshConst = 0.03
pathThresh = 0
longPaths = []  

rowCursor = arcpy.SearchCursor(points)

arcpy.MakeTableView_management(points, "myTableView")
total = int(arcpy.GetCount_management("myTableView").getOutput(0))
pathThresh = total * threshConst

with arcpy.da.UpdateCursor(points, ["Track_deg_", "Elevation_", "Path_Num"]) as cursor: # @UndefinedVariable
    for row in cursor:
        
        currDegree = row[0]
        if (abs(currDegree - prevDegree) >= 90):
            
            if (pathLen[pathNum] >= pathThresh):
                longPaths.append(pathNum)
            
            pathNum += 1
            row[2] = pathNum
            if (pathLen.has_key(pathNum)):
                pathLen[pathNum] += 1   
            else:
                pathLen[pathNum] = 1
            cursor.updateRow(row)
            prevDegree = currDegree
             
        else:
            row[2] = pathNum
            if (pathLen.has_key(pathNum)):
                pathLen[pathNum] += 1   
            else:
                pathLen[pathNum] = 1
            cursor.updateRow(row)
            prevDegree = currDegree
            
            
# def shortenPath(path, deg):
#     pathNum = path
#     prevDegree = deg
#     totPoints = 0
#     with arcpy.da.UpdateCursor(points, ["Track_deg_", "Elevation_", "Path_Num"], '"Path_Num" = {0}'.format(path)) as cursor: # @UndefinedVariable
#         currDegree = row[0]
#         if (abs(currDegree - prevDegree) >= deg):
#             pathNum += 1
#             row[2] = pathNum
#             cursor.updateRow(row)
#             prevDegree = currDegree
#              
#         else:
#             row[2] = pathNum
#             totPoints += 1
#             cursor.updateRow(row)
#             prevDegree = currDegree
#             
#     return totPoints
#         
#             
#             
# for key in longPaths:
#     deg = 90
#     while(pathLen[key] >= pathThresh):
#         deg = deg - 5
#         pathLen[key] = shortenPath(key, deg)
#         
#     print pathLen[key]
        
    
          
