import arcpy

lioInput = arcpy.GetParameterAsText(0)

inputFields = ['SOIL_NAME1', 'CLI1', 'CLI1_1', 'CLI1_2', 'CLI2', 'CLI2_1', 'CLI2_2', 'CLI3', 'CLI3_1', 'CLI3_2', 'CLI1_Conc', 'CLI2_Conc', 'CLI3_Conc']
cli1FieldName = 'CLI1_Conc'
cli2FieldName = 'CLI2_Conc'
cli3FieldName = 'CLI3_Conc'

if (len(arcpy.ListFields(lioInput, cli1FieldName)) == 0):
    arcpy.AddField_management(lioInput, cli1FieldName, "STRING")
    
if (len(arcpy.ListFields(lioInput, cli2FieldName)) == 0):
    arcpy.AddField_management(lioInput, cli2FieldName, "STRING")
    
if (len(arcpy.ListFields(lioInput, cli3FieldName)) == 0):
    arcpy.AddField_management(lioInput, cli3FieldName, "STRING")

with arcpy.da.UpdateCursor(lioInput, inputFields) as cursor:
    
    for row in cursor:
        if (row[1] == " "):
            row[10] = "ERROR"
            row[11] = "ERROR"
            row[12] = "ERROR"
            
            cursor.updateRow(row)
            
        else:    
        
            cli1Conc = "".join([row[1], row[2], row[3]])
            cli2Conc = "".join([row[4], row[5], row[6]])
            cli3Conc = "".join([row[7], row[8], row[9]])
            
            row[10] = cli1Conc
            row[11] = cli2Conc
            row[12] = cli3Conc
            
            cursor.updateRow(row)
        
    