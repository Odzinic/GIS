import arcpy
import os


fcIn = r"J:\Scripts\GIS\LIO_SoilCompare\Assessments.gdb\Points\LIOEditor_Point"
comparetblIn = r"J:\Scripts\GIS\LIO_SoilCompare\Assessments.gdb\Compare_Results"
outGDB = r"J:\Scripts\GIS\LIO_SoilCompare\Assessments.gdb"
outTbl = os.path.join(outGDB, "FieldChange_Freq")

fcLayer = arcpy.mapping.Layer(fcIn)
fcFields = arcpy.ListFields(fcIn)
fcNames = {}

for field in fcFields:
    fcNames[field.name] = 0
    
with arcpy.da.SearchCursor(comparetblIn, ["Message"]) as cursor:
    for row in cursor:
        message = row[0]
        messageField = message.split(" ")[-1]
        try:
            fcNames[messageField] += 1
        except KeyError:
            pass
    
arcpy.CreateTable_management(outGDB, "FieldChange_Freq", fcIn)
for field in arcpy.ListFields(outTbl):
    if (field.length < 10):
        try:
            arcpy.AlterField_management(outTbl, field.name, "", "", "TEXT", "10")

        except arcpy.ExecuteError:
            pass
            
rows = arcpy.InsertCursor(outTbl)
row = rows.newRow()
for field in fcNames.keys():
    try:
        row.setValue(field, str(fcNames[field]))
    except RuntimeError:
        pass
rows.insertRow(row)
