import arcpy
from arcpy import sa as arcs
import os
import xlwt

arcpy.CheckOutExtension('Spatial')

main_dir = os.getcwd()
image_dir = os.path.join(main_dir, "Image_Input")
mask_dir = os.path.join(main_dir, "Buffers")

if not os.path.exists(os.path.join(main_dir, "Output")):                                # Check to see if output folder exists and creates one if not
    os.makedirs(os.path.join(main_dir, "Output"))
out_dir = os.path.join(main_dir, "Output")

if not os.path.exists(os.path.join(main_dir, "Temp")):                                  # Check to see if temp folder exists and creates one if not
    os.makedirs(os.path.join(main_dir, "Temp"))
temp_dir = os.path.join(main_dir, "Temp")



masks = os.listdir(mask_dir)
buffers = filter((lambda x: x.endswith(".shp")), masks)
class_img = os.path.join(image_dir, os.listdir(image_dir)[0])
outResult = os.path.join(out_dir, "Results.xls")

book = xlwt.Workbook()
sh = book.add_sheet("Sheet")

total = 0
allValues = {}
missClass = []
i = -1
q = 0


#for bfr in buffers:
#    maskName = str(bfr).strip(".shp")
#
#    extractMask = arcs.ExtractByMask(class_img, os.path.join(mask_dir, bfr))
#    extractMask.save(os.path.join(temp_dir, "{0}_clipped.tif".format(maskName)))
#    
    

clipImg = filter((lambda x: x.endswith(".tif")), os.listdir(temp_dir))
   
for img in clipImg:
    imgPath = os.path.join(temp_dir, img)
    fieldCursor = arcpy.SearchCursor(imgPath)
    valueField = arcpy.ListFields(imgPath, "Value")
    countField =  arcpy.ListFields(imgPath, "Count")
    
    for row in fieldCursor:
        allValues[int(row.getValue(valueField[0].name))] = []
        
    allClasses = sorted(allValues.keys())
    

for img in clipImg:
    imgPath = os.path.join(temp_dir, img)
    fieldCursor = arcpy.SearchCursor(imgPath)
    valueField = arcpy.ListFields(imgPath, "Value")
    countField =  arcpy.ListFields(imgPath, "Count")
    
    for row in fieldCursor:
        total = total + row.getValue(countField[0].name)
               
    fieldCursor = arcpy.SearchCursor(imgPath)  
    for row in fieldCursor:
        allValues[int(row.getValue(valueField[0].name))].append(float(row.getValue(countField[0].name)) / total)
        missClass.append(int(row.getValue(valueField[0].name)))
    
    if (sorted(missClass) != allClasses):
        print sorted(missClass)
        print allClasses
        print ""
        diff = list(set(allClasses).difference(missClass))
        for key in diff:
            print key
            allValues[int(key)].append(0.0)
    missClass = []      
    total = 0       

sortedValues = sorted(allValues.keys())

#text_file = open(outResult, "w")

for key in sortedValues:
    for value in allValues[key]:
        i = i + 1
        sh.write(i, q, value)
    q = q + 1
    i = -1
        
book.save(outResult)