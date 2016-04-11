import arcpy

lioInput = arcpy.GetParameterAsText(0)
slopeClass1 = arcpy.GetParameterAsText(1)
slopeCLI1 = arcpy.GetParameterAsText(2)

try:
    slopeClass2 = arcpy.GetParameterAsText(3)
    slopeCLI2 = arcpy.GetParameterAsText(4)
except RuntimeError:
    slopeClass2 = ""
    slopeCLI2 = ""
    
try:
    slopeClass3 = arcpy.GetParameterAsText(5)
    slopeCLI3 = arcpy.GetParameterAsText(6)
except RuntimeError:
    slopeClass3 = ""
    slopeCLI3 = ""

classLst = ['1','2','3','4','5','6','7']
classKeys = {'F': '5',
             'f': '5',
             'G': '6',
             'g': '6',
             'H': '7',
             'I': '7',
             'J': '7',
             'h': '7',
             'i': '7',
             'j': '7'}

slopecheckField1 = "Slope_Check1"
slopecheckField2 = "Slope_Check2"
slopecheckField3 = "Slope_Check3"

if (len(arcpy.ListFields(lioInput, slopecheckField1)) == 0):
    arcpy.AddField_management(lioInput, slopecheckField1, "SHORT")
    
with arcpy.da.UpdateCursor(lioInput, [slopeClass1, slopeCLI1, slopecheckField1]) as cursor:
    for row in cursor:
        
        if (row[0] == 'F' or row[0] == 'f'):
            bestCLI = classKeys[row[0]]
            if (row[1] in classLst[:classLst.index(bestCLI)]):
                row[2] = 1
                
            else:
                row[2] = 0
                
        if (row[0] == 'G' or row[0] == 'g'):
            bestCLI = classKeys[row[0]]
            if (row[1] in classLst[:classLst.index(bestCLI)]):
                row[2] = 1
                
            else:
                row[2] = 0
                
        if (row[0] == 'H' or row[0] == 'h'):
            bestCLI = classKeys[row[0]]
            if (row[1] in classLst[:classLst.index(bestCLI)]):
                row[2] = 1
                
            else:
                row[2] = 0
                
        if (row[0] == 'I' or row[0] == 'i'):
            bestCLI = classKeys[row[0]]
            if (row[1] in classLst[:classLst.index(bestCLI)]):
                row[2] = 1
                
            else:
                row[2] = 0
                
        if (row[0] == 'J' or row[0] == 'j'):
            bestCLI = classKeys[row[0]]
            if (row[1] in classLst[:classLst.index(bestCLI)]):
                row[2] = 1
                
            else:
                row[2] = 0
                
        cursor.updateRow(row)
    del cursor
 
 
 
        
if (slopeClass2 != "" and slopeCLI2 != ""):
    if (len(arcpy.ListFields(lioInput, slopecheckField2)) == 0):
        arcpy.AddField_management(lioInput, slopecheckField2, "SHORT")
        
    with arcpy.da.UpdateCursor(lioInput, [slopeClass2, slopeCLI2, slopecheckField2]) as cursor:
        for row in cursor:
            if (row[0] == 'F' or row[0] == 'f'):
                bestCLI = classKeys[row[0]]
                if (row[1] in classLst[:classLst.index(bestCLI)]):
                    row[2] = 1
                    
                else:
                    row[2] = 0
                    
            if (row[0] == 'G' or row[0] == 'g'):
                bestCLI = classKeys[row[0]]
                if (row[1] in classLst[:classLst.index(bestCLI)]):
                    row[2] = 1
                    
                else:
                    row[2] = 0
                    
            if (row[0] == 'H' or row[0] == 'h'):
                bestCLI = classKeys[row[0]]
                if (row[1] in classLst[:classLst.index(bestCLI)]):
                    row[2] = 1
                    
                else:
                    row[2] = 0
                    
            if (row[0] == 'I' or row[0] == 'i'):
                bestCLI = classKeys[row[0]]
                if (row[1] in classLst[:classLst.index(bestCLI)]):
                    row[2] = 1
                    
                else:
                    row[2] = 0
                    
            if (row[0] == 'J' or row[0] == 'j'):
                bestCLI = classKeys[row[0]]
                if (row[1] in classLst[:classLst.index(bestCLI)]):
                    row[2] = 1
                    
                else:
                    row[2] = 0
                    
            cursor.updateRow(row)
        del cursor    
            
if (slopeClass3 != "" and slopeCLI3 != ""):
    if (len(arcpy.ListFields(lioInput, slopecheckField3)) == 0):
        arcpy.AddField_management(lioInput, slopecheckField3, "SHORT")
        
    with arcpy.da.UpdateCursor(lioInput, [slopeClass3, slopeCLI3, slopecheckField3]) as cursor:
        for row in cursor:
            if (row[0] == 'F' or row[0] == 'f'):
                bestCLI = classKeys[row[0]]
                if (row[1] in classLst[:classLst.index(bestCLI)]):
                    row[2] = 1
                    
                else:
                    row[2] = 0
                    
            if (row[0] == 'G' or row[0] == 'g'):
                bestCLI = classKeys[row[0]]
                if (row[1] in classLst[:classLst.index(bestCLI)]):
                    row[2] = 1
                    
                else:
                    row[2] = 0
                    
            if (row[0] == 'H' or row[0] == 'h'):
                bestCLI = classKeys[row[0]]
                if (row[1] in classLst[:classLst.index(bestCLI)]):
                    row[2] = 1
                    
                else:
                    row[2] = 0
                    
            if (row[0] == 'I' or row[0] == 'i'):
                bestCLI = classKeys[row[0]]
                if (row[1] in classLst[:classLst.index(bestCLI)]):
                    row[2] = 1
                    
                else:
                    row[2] = 0
                    
            if (row[0] == 'J' or row[0] == 'j'):
                bestCLI = classKeys[row[0]]
                if (row[1] in classLst[:classLst.index(bestCLI)]):
                    row[2] = 1
                    
                else:
                    row[2] = 0
                    
            cursor.updateRow(row)
        del cursor        
        