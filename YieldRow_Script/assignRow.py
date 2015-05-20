import os
import arcpy
from arcpy import sa as arcs
from arcpy import da as arcda
import numpy as np
arcpy.CheckOutExtension('Spatial')                                                      # Verifies that the Spatial Analyst extension is activated
print "Imported arcpy"

np.seterr(all='ignore')

input_dir = os.path.join(os.getcwd(), "input")

inputs = os.listdir(input_dir)                                                            # List that loads all files in the mask/buffer directory
# points = os.path.join(input_dir, filter((lambda x: x.endswith(".shp")), inputs)[0])       # Loads only shapefile masks/buffers to prevent useless files
points = r"I:\Scripts\GIS\YieldRow_Script\input\Randy Cain-Home-All-2014-Harvest-Harvest-Corn.shp"

pointDic = {}
currDegree = 0
prevDegree = 50
pathNum = 1
pathLen = {}
threshConst = 0.025
pathThresh = 0
longPaths = []


arcpy.MakeTableView_management(points, "myTableView")
total = int(arcpy.GetCount_management("myTableView").getOutput(0))
pathThresh = total * threshConst


with arcpy.da.SearchCursor(points, ["FID", "Heading", "DryYield", "Path_Num"]) as cursor: # @UndefinedVariable
    for row in cursor:
        pointDic[row[0]] = [row[1], row[2], row[3], 0]

if (pointDic[0][0] >= 50):
    pathNum = 0    
        
for key in pointDic.keys():
        row = pointDic[key]
        currDegree = row[0]
        
        if (abs(currDegree - prevDegree) >= 50):
            try:
#                 lookahCheck = (abs((pointDic[key + 10][0] - currDegree)) < abs((pointDic[key + 10][0] - prevDegree)))
                lookahCheck = (abs((pointDic[key + 5][0] - currDegree)) < (abs(currDegree - prevDegree)))
            except KeyError:
                lookahCheck = (abs((pointDic[pointDic.keys()[-1]][0] - currDegree)) < abs((pointDic[pointDic.keys()[-1]][0] - prevDegree)))
            
            if (lookahCheck):
                
                if (pathLen.has_key(pathNum)):
                    pathLen[pathNum] += 1   
                else:
                    pathLen[pathNum] = 1
                    
                if (pathLen[pathNum] >= pathThresh):
                    longPaths.append(pathNum)
                    
                
                    
                pathNum += 1
                row[2] = pathNum
                
                 
                prevDegree = currDegree
                
            else:
                print "false positive"
                row[2] = pathNum
                if (pathLen.has_key(pathNum)):
                    pathLen[pathNum] += 1   
                else:
                    pathLen[pathNum] = 1
                prevDegree = currDegree
              
        else:
            row[2] = pathNum
            if (pathLen.has_key(pathNum)):
                pathLen[pathNum] += 1   
            else:
                pathLen[pathNum] = 1
            prevDegree = currDegree
            
# for path in longPaths:
#     longKeys = []
#     for row in pointDic.items():
#         if row[1][2] == path:
#             longKeys.append(row[0])
#         
#     print pointDic[longKeys[0]]    
#     prevDegree = pointDic[longKeys[0]][0]
#     pathNum = path
#     for key in longKeys:
#         currDegree = pointDic[key][0]
#         if (abs(currDegree - prevDegree) >= 9):
#             print "Path changed"                    
#             pathNum += 100
#             pointDic[key][2] = pathNum
#              
#             prevDegree = currDegree
#         
#         else:
#             pointDic[key][2] = pathNum
#             prevDegree = currDegree
globYield = arcpy.da.TableToNumPyArray(points, ["DryYield"]) # @UndefinedVariable
globMean = np.mean(globYield["DryYield"])
globSTD = np.std(globYield["DryYield"])
globuppThresh = globMean + (2*globSTD)
globlowThresh = globMean - (1.2*globSTD)
print globMean, globSTD, globuppThresh, globlowThresh

for path in pathLen.keys():
    locYield = globYield = arcpy.da.TableToNumPyArray(points, ["DryYield"], '"Path_Num" = {0}'.format(path))
    locMean = np.mean(locYield["DryYield"])
    locSTD = np.std(locYield["DryYield"])
    locuppThresh = locMean + (2*locSTD)
    loclowThresh = locMean - (1.2*locSTD)
    
    for key in filter((lambda x: pointDic[x][2] == path), pointDic.keys()):
        if (pointDic[key][2] < loclowThresh and pointDic[key][2] > locuppThresh):
            pointDic[key][3] = 1 
          
with arcpy.da.UpdateCursor(points, ["FID", "Heading", "Elevatio", "Path_Num", "DryYield"]) as cursor: # @UndefinedVariable
    for row in cursor:
        if (row[4] > globlowThresh and row[4] < globuppThresh and pointDic[row[0]][3] == 0):
            row[3] = pointDic[row[0]][2]
            cursor.updateRow(row)
        
        else:
            cursor.deleteRow()
            
            
            
pointDic = {}
currDegree = 0
prevDegree = 50
pathNum = 1
pathLen = {}
threshConst = 0.025
pathThresh = 0
longPaths = []
            
with arcpy.da.SearchCursor(points, ["FID", "Heading", "DryYield", "Path_Num"]) as cursor: # @UndefinedVariable
    for row in cursor:
        pointDic[row[0]] = [row[1], row[2], row[3], 0]

if (pointDic[0][0] >= 50):
    pathNum = 0    
        
for key in pointDic.keys():
        row = pointDic[key]
        currDegree = row[0]
        
        if (abs(currDegree - prevDegree) >= 50):
            try:
#                 lookahCheck = (abs((pointDic[key + 10][0] - currDegree)) < abs((pointDic[key + 10][0] - prevDegree)))
                lookahCheck = (abs((pointDic[key + 5][0] - currDegree)) < (abs(currDegree - prevDegree)))
            except KeyError:
                lookahCheck = (abs((pointDic[pointDic.keys()[-1]][0] - currDegree)) < abs((pointDic[pointDic.keys()[-1]][0] - prevDegree)))
            
            if (lookahCheck):
                
                if (pathLen.has_key(pathNum)):
                    pathLen[pathNum] += 1   
                else:
                    pathLen[pathNum] = 1
                    
                if (pathLen[pathNum] >= pathThresh):
                    longPaths.append(pathNum)
                    
                
                    
                pathNum += 1
                row[2] = pathNum
                
                 
                prevDegree = currDegree
                
            else:
                print "false positive"
                row[2] = pathNum
                if (pathLen.has_key(pathNum)):
                    pathLen[pathNum] += 1   
                else:
                    pathLen[pathNum] = 1
                prevDegree = currDegree
              
        else:
            row[2] = pathNum
            if (pathLen.has_key(pathNum)):
                pathLen[pathNum] += 1   
            else:
                pathLen[pathNum] = 1
            prevDegree = currDegree
            
with arcpy.da.UpdateCursor(points, ["FID", "Heading", "Elevatio", "Path_Num", "DryYield"]) as cursor: # @UndefinedVariable
    for row in cursor:
        row[3] = pointDic[row[0]][2]
        cursor.updateRow(row)