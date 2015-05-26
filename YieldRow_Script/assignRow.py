
''' Imports '''
import os
import arcpy
import numpy as np
arcpy.CheckOutExtension('Spatial')                                                      # Verifies that the Spatial Analyst extension is activated
print "Imported arcpy"

np.seterr(all='ignore')                                                                 # Suppresses numpy warnings


''' Directories '''
# input_dir = os.path.join(os.getcwd(), "input")                                          

# inputs = os.listdir(input_dir)                                                            # List that loads all files in the mask/buffer directory
points = arcpy.GetParameterAsText(0)
# points = os.path.join(input_dir, filter((lambda x: x.endswith(".shp")), inputs)[0])       # Loads only shapefile masks/buffers to prevent useless files
# points = r"I:\Scripts\GIS\YieldRow_Script\projected\Randy Cain-Home-All-2014-Harvest-Harvest-Corn.shp"
inputName = points.split('\\')[-1]
inputName = inputName.replace('-', '')
# tableDir = r"I:\Scripts\GIS\YieldRow_Script\table_test"
tableDir = arcpy.GetParameter(1)



''' Constants '''
pointDic = {}                                                                           # Dictionary used to store all points from shapefile
currDegree = 0                                                                          # Variable that saves the direction degree of current point
prevDegree = 50                                                                         # Variable that saves the direction degree of previous point
                                                                                        # default set to the degree threshold
pathNum = 1                                                                             # Variable that stores the current path/load number
pathLen = {}
threshConst = 0.025
pathThresh = 0
longPaths = []
degreeField = arcpy.GetParameterAsText(2)
yieldField = arcpy.GetParameterAsText(3)
upperSTD = arcpy.GetParameter(4)
lowerSTD = arcpy.GetParameter(5)


# arcpy.MakeTableView_management(points, "myTableView")
# total = int(arcpy.GetCount_management("myTableView").getOutput(0))
# pathThresh = total * threshConst
#  

arcpy.AddField_management(points, "Path_Num", "SHORT")                                  # Add a field for the path number

# SearchCursor goes through all the points in the input shapefile
# and saves the FID(key), degree(value 1), yield(value 2) and creates a variable for path number(value 3)
# in a dictionary 
with arcpy.da.SearchCursor(points, ["FID", degreeField, yieldField, "Path_Num"]) as cursor: # @UndefinedVariable
    for row in cursor:
        pointDic[row[0]] = [row[1], row[2], row[3], 0]                                  # Storing each tuple in dictionary with the FID being the key
 
if (pointDic[0][0] >= 50):
    pathNum = 0    


# Iterates through every tuple that was stored in the dictionary
# and checks whether the degree delta is 50 or more. If true,
# the path number(pathNum) increases by one and is assigned to
# the tuple         
for key in pointDic.keys():                                                             # Iterate through all of the keys in the point dictionary(pointDic)
        row = pointDic[key]                                                             # Retrieves and stores all of the stored values for that key
        currDegree = row[0]                                                             # Retrieves the degree value from the current tuple
         
        if (abs(currDegree - prevDegree) >= 50):                                        # Checks to see if the degree difference is 50 or more
            
            
            
            
            # Checks to see if the point 5 after the current point has a smaller difference
            # than the difference between current and past to prevent spurious tuples from
            # making the path number increase
            # NOTE: The try/except prevents out of bound list errors by grabbing the last
            # value in the list if an out of bound error occurs
            try:
                lookahCheck = (abs((pointDic[key + 5][0] - currDegree)) < 
                               (abs(currDegree - prevDegree)))
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
             

globYield = arcpy.da.TableToNumPyArray(points, [yieldField]) # @UndefinedVariable
globMean = np.mean(globYield[yieldField])
globSTD = np.std(globYield[yieldField])
globuppThresh = globMean + (upperSTD*globSTD)
globlowThresh = globMean - (lowerSTD*globSTD)
print globMean, globSTD, globuppThresh, globlowThresh
 
for path in pathLen.keys():
    locYield = globYield = arcpy.da.TableToNumPyArray(points, [yieldField], '"Path_Num" = {0}'.format(path))
    locMean = np.mean(locYield[yieldField])
    locSTD = np.std(locYield[yieldField])
    locuppThresh = locMean + (upperSTD*locSTD)
    loclowThresh = locMean - (lowerSTD*locSTD)
     
    for key in filter((lambda x: pointDic[x][2] == path), pointDic.keys()):
        if (pointDic[key][2] < loclowThresh and pointDic[key][2] > locuppThresh):
            pointDic[key][3] = 1 
           
with arcpy.da.UpdateCursor(points, ["FID", degreeField, "Elevatio", "Path_Num", yieldField]) as cursor: # @UndefinedVariable
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
             
with arcpy.da.SearchCursor(points, ["FID", degreeField, yieldField, "Path_Num"]) as cursor: # @UndefinedVariable
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
                precvDegree = currDegree
               
        else:
            row[2] = pathNum
            if (pathLen.has_key(pathNum)):
                pathLen[pathNum] += 1   
            else:
                pathLen[pathNum] = 1
            prevDegree = currDegree
             
with arcpy.da.UpdateCursor(points, ["FID", degreeField, "Elevatio", "Path_Num", yieldField ]) as cursor: # @UndefinedVariable
    for row in cursor:
        row[3] = pointDic[row[0]][2]
        cursor.updateRow(row)

arcpy.AddXY_management(points)
arcpy.AddField_management(points, "Obj_ID", "LONG")
arcpy.CalculateField_management(points, "Obj_ID", "!FID!", "PYTHON")
         
tableMapp = arcpy.FieldMappings()

tableFields = arcpy.FieldMap()
tableFields.addInputField(points, "POINT_X")
tableMapp.addFieldMap(tableFields)
tableFields = arcpy.FieldMap()
tableFields.addInputField(points, "POINT_Y")
tableMapp.addFieldMap(tableFields)
tableFields = arcpy.FieldMap()
tableFields.addInputField(points, "Obj_ID")
tableMapp.addFieldMap(tableFields)
tableFields = arcpy.FieldMap()
tableFields.addInputField(points, yieldField)
tableMapp.addFieldMap(tableFields)
tableFields = arcpy.FieldMap()
tableFields.addInputField(points, "Path_Num") 
tableMapp.addFieldMap(tableFields)



arcpy.TableToTable_conversion(points, tableDir, inputName[:inputName.index(".shp")],'',  tableMapp)