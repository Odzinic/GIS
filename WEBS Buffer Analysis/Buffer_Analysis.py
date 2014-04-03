'''
Created by Omar Dzinic (Omar.Dzinic@agr.gc.ca)
April 3, 2014

'''


''' Imports '''
import arcpy
from arcpy import sa as arcs
import os
import xlwt
import shutil

arcpy.CheckOutExtension('Spatial')                                                      # Verifies that the Spatial Analyst extension is activated


''' Directories '''
main_dir = os.getcwd()                                                                  # Directory which the script is located in
image_dir = os.path.join(main_dir, "Image_Input")                                       # Image directory
mask_dir = os.path.join(main_dir, "Buffers")                                            # Mask/buffer directory

if not os.path.exists(os.path.join(main_dir, "Output")):                                # Check to see if output folder exists and creates one if not
    os.makedirs(os.path.join(main_dir, "Output"))
out_dir = os.path.join(main_dir, "Output")

if not os.path.exists(os.path.join(main_dir, "Temp")):                                  # Check to see if temp folder exists and creates one if not
    os.makedirs(os.path.join(main_dir, "Temp"))
else:
    shutil.rmtree(os.path.join(main_dir, "Temp"))                                       # If the temp directory contains old temp files, deletes them
    os.makedirs(os.path.join(main_dir, "Temp"))

temp_dir = os.path.join(main_dir, "Temp")                                               # Temp working directory


''' Constants '''
masks = os.listdir(mask_dir)                                                            # List that loads all files in the mask/buffer directory
buffers = filter((lambda x: x.endswith(".shp")), masks)                                 # Loads only shapefile masks/buffers to prevent useless files
                                                                                        # from crashing the program
                                                                                        
class_img = os.path.join(image_dir, os.listdir(image_dir)[0])                           # Loads the TIFF located in the image directory
outResult = os.path.join(out_dir, "Results.xls")                                        # Directory for output Excel file                                        

book = xlwt.Workbook()                                                                  # Creates an Excel workbook
sh = book.add_sheet("Sheet")                                                            # Adds a sheet to the workbook
bold = xlwt.easyxf('font: bold True;')                                                  # Bold font for headings in the Excel file

fieldTotal = 0                                                                          # Used to find the sum of each field
allValues = {}                                                                          # Dictionary that contains the values for each class in
                                                                                        # the clipped image. In format, {class: [values]}

missClass = []                                                                          # List that is used to check if any of the standard classes
                                                                                        # is missing from the image to prevent that class not having
                                                                                        # 0 instances

i = 1
q = 0
z = 1


''' Clip image to masks'''
# Process clips the input image using all of the mask
# shapefiles in the masks directory and creates a TIFF
# for each clip. Uses the mask's name as the output file
# name.

print "Clipping images"

for bfr in buffers:                                                                     # Iterates through all of the masks in the masks directory
    maskName = str(bfr).strip(".shp")                                                   # Removes ".shp" from the fine name to be used for clip output

    extractMask = arcs.ExtractByMask(class_img, os.path.join(mask_dir, bfr))            # Uses Extract by Mask to clip the input image to each mask
    extractMask.save(os.path.join(temp_dir, "{0}_clipped.tif".format(maskName)))        # Saves the clip as "(CLIP_NAME)_clipped.tif" in temp directory
    
    

''' Create dictionary keys for classes '''
# Creates a dictionary that contains every class that
# exists in the image and assigns an empty list to it
# for the pixel counts

print "Creating dictionary keys for classes"

clipImg = filter((lambda x: x.endswith(".tif")), os.listdir(temp_dir))                  # Filters the temp directory and loads all of the clipped TIFFs
   
for img in clipImg:                                                                     # Iterates through all of the clipped TIFFs
    imgPath = os.path.join(temp_dir, img)                                               # Creates a path to the current TIFF
    fieldCursor = arcpy.SearchCursor(imgPath)                                           # Search cursor for the image is created to allow analysis of
                                                                                        # fields
    
    valueField = arcpy.ListFields(imgPath, "Value")                                     # Creates list of all of the classes in the clipped image
    countField = arcpy.ListFields(imgPath, "Count")                                     # Creates list of the pixel counts for each class in the clipped
                                                                                        # image
    
    for row in fieldCursor:
        allValues[int(row.getValue(valueField[0].name))] = []                           # Creates a key for every class and assigns an empty list to it
        
    allClasses = sorted(allValues.keys())                                               # Sorts the keys from smallest values to largest (ex. 20 (Water)
                                                                                        # is before 34 (Developed))

''' Calculate values'''
# Finds the percentage of a every class in a clipped
# image and saves it to the proper location in allValues
    
print "Calculating values for classes"

for img in clipImg:
    imgPath = os.path.join(temp_dir, img)                                               # Creates a path to the current TIFF
    fieldCursor = arcpy.SearchCursor(imgPath)                                           # Search cursor for the image is created to allow analysis of
                                                                                        # fields
    
    valueField = arcpy.ListFields(imgPath, "Value")                                     # Creates list of all of the classes in the clipped image
    countField = arcpy.ListFields(imgPath, "Count")                                     # Creates list of the pixel counts for each class in the clipped
                                                                                        # image
    
    for row in fieldCursor:
        fieldTotal = fieldTotal + row.getValue(countField[0].name)                      # Variable that collects the total sum of pixels in an image
               
    fieldCursor = arcpy.SearchCursor(imgPath)  
    for row in fieldCursor:
        allValues[int(row.getValue(valueField[0].name))].append(float(row.getValue(countField[0].name)) / fieldTotal)
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
    fieldTotal = 0       

sortedValues = sorted(allValues.keys())

''' Creates headings for every mask '''
for msk in clipImg:
    sh.write(0, z, msk.strip("_clipped.tif"), bold)                                     # Writes heading in first row in bold
    z = z + 1

''' Writes calculated values to Excel '''
    
print "Writing values to file"  
  
for key in sortedValues:
    sh.write(i, q, key, bold)                                                           # Writes the current class number
    for value in allValues[key]:
        q = q + 1
        sh.write(i, q, value)                                                           # Writes values for each class
    i = i + 1
    q = 0
        
book.save(outResult)                                                                    # Saves the Excel file to the outResult path

print "Values saved in {0}".format(outResult)
print "Process complete"
