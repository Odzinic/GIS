# -*- coding: utf-8 -*-

'''
Created by Omar Dzinic (Omar.Dzinic@agr.gc.ca)
March 11, 2014

'''


'''Imports'''
import arcpy 
import arcpy.mapping as arcm
import os
from shutil import copyfile
import datetime
import re



'''Directories'''
main_dir = os.getcwd()                                                                  # Directory of script
img_dir = os.path.join(main_dir, "Input_Image")                                         # Directory for input image
template_dir = os.path.join(main_dir, "Input_Template")                                 # Directory for input template
vector_dir = os.path.join(main_dir, "Input_Vectors")                                    # Directory for shapefiles

if not os.path.exists(os.path.join(main_dir, "Output")):                                # Check to see if output folder exists and creates one if not
    os.makedirs(os.path.join(main_dir, "Output"))
out_dir = os.path.join(main_dir, "Output")                                              # Directory for output mxd and pdf




'''Constants'''
in_img = os.listdir(img_dir)[0]
print "Input image is {0}".format(in_img)

in_template = os.listdir(template_dir)[0]
print "Input template is {0}".format(in_template)

print "The output directory is {0}".format(out_dir)

copyfile(os.path.join(template_dir, in_template), os.path.join(out_dir, in_template))   # Copies template from the template directory to output
mxd = arcpy.mapping.MapDocument(os.path.join(out_dir, in_template))                     # Copied template to be used in script

listDframe = arcm.ListDataFrames(mxd)                                                   # Loop through all of the data frames
for frame in listDframe:                                                                # in the template and finds the Climate
    if (frame.name == "Climate Map"):                                                   # Map data frame
        testDframe = frame

tiffInput = os.path.join(img_dir, str(os.listdir(img_dir)[0]))                          # The input tiff image
tiffOutput = os.path.join(vector_dir, "temp.tif")                                       # The path to the temp copy of the tiff image

englishMonth = ['January', 'February', 'March', 'April', 'May', 'June', 'July',         # List of months
                'August', 'September', 'October', 'November', 'December']               # in English for date                                                                                                                                         

frenchMonth = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',         # List of months
               'août', 'septembre', 'octobre', 'novembre', 'décembre']                   # in French for date

totalDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]                            # List of total days for every month

monthlyText = "{0} 1 - {1}, {2} / 1 - {1} {3}, {2}"
biweeklyText = "Week {0} and {1} ({2} {3} - {4} {5}), {6} / Semaine {0} et {1} ({3} {7} au {5} {8}), {6}"
weeklyText = "Week {0} ({1} {2} - {1} {3}), {4} / Semaine {0} ({5} {6} au {5} {7}), {4}"

monthlyOut = "SMOS_SM_{0}_Month{1}_NorthAmerica.pdf"
biweeklyOut = "SMOS_SM_{0}_BiWeek{1}-{2}_National.pdf"
weeklyOut = "SMOS_SM_{0}_Week{1}_25D_National.pdf"




copyfile(tiffInput, tiffOutput)                                                         # Create temp of the tiff image and put it in vectors directory



'''Reproject tiff'''
# Projects a raster to a specific coordinate system. 

# NOTE: Disabled by default. Can be uncommented and used. Change the
# projection variable to what the output coordinate system should be
# and inproj to what the current projection is

#if os.path.exists(tiffOutput):
#    os.remove(tiffOutput)
#
#reprojTif = filter(lambda x: str(x).endswith(".tif"), arcm.ListLayers(mxd))[0]
fname = str(in_img)
#
#arcpy.ProjectRaster_management(tiffInput, tiffOutput, projection, "", "28000", "NAD_1983_To_WGS_1984_1", "", inproj)
#
#os.remove(tiffInput)
#os.rename(tiffOutput, tiffInput)




'''Set data paths'''
# Procedure fixes the data sources of layers to prevent the layers from "missing" in ArcMap
# after using template on another computer

print "Fixing data sources"

for lyr in arcm.ListLayers(mxd):                                                        # Loops through all layers in the template
    name = str(lyr)                                                                     # Name of current layer in loop
    arcm.RemoveLayer(testDframe, lyr)                                                   # Removes the layer from the data frame
    if ((lyr.dataSource).endswith(".tif")):                                             # Checks to see if layer is a tiff image to prevent compatibility
        lyr.replaceDataSource(vector_dir, "RASTER_WORKSPACE", "temp.tif")               # issues with changing the data source. Then changes the data source
    else:
        lyr.replaceDataSource(vector_dir, "SHAPEFILE_WORKSPACE", name)                  # Changes data source of shapefiles
    arcm.AddLayer(testDframe, lyr, "AUTO_ARRANGE")                                      # Adds the updated layer to the data frame
    
    



'''Change the week number and date'''
# Converts the week number and year that is extracted from the image name
# into a Gregorian calendar date. Then uses the date to update the date text
# field in the map

# NOTE: The input image must be named using the following format:
# GlobAv_SMUDP2_OPER_551_(YEAR_NUM)_Week_(WEEK_NUM)WGS84.tif where YEAR_NUM
# is the year (xxxx) and WEEK_NUM is the week number (xx)

print "Changing date information"

splitFname = fname.split("_")
yearNum = int(splitFname[4])                                                            # Extracts the year number from the image name
for txt in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
    if txt.name == "Week Info":
        dateText = txt

def iso_year_start(iso_year):                                                           # The Gregorian calendar date of the first day of the given ISO year
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday() - 1)
    return fourth_jan - delta 

def iso_to_gregorian(iso_year, iso_week, iso_day):                                      # Gregorian calendar date for the given ISO year, week and day
    year_start = iso_year_start(iso_year)
    return year_start + datetime.timedelta(days=iso_day - 1, weeks=iso_week - 1)


# Date modifier for monthly maps
if (splitFname[5] == "Month"):
    if (re.search('[a-zA-Z]', splitFname[6][0:2])):
        monthNum = int(splitFname[6][0:1])
    else:
        monthNum = int(splitFname[6][0:2])
    dateText.text = monthlyText.format(englishMonth[monthNum - 1], 
                                       totalDays[monthNum - 1],
                                       yearNum, frenchMonth[monthNum - 1])
    fnameOut = monthlyOut.format(yearNum, monthNum)
        
# Date modifier for bi-weekly maps
elif (splitFname[5] == "Bi-week"):
    if (re.search('[a-zA-Z]', splitFname[6][0:2])):
        weekNum = int(splitFname[6][0:1])
    else:
        weekNum = int(splitFname[6][0:2])
    
    firstDate = str(iso_to_gregorian(yearNum, weekNum, 1)).split("-")
    endDate = str(iso_to_gregorian(yearNum, weekNum + 1, 1)).split("-")
    
    if((int(endDate[2]) + 6) > totalDays[int(endDate[1]) - 1]):
        firstMonth = int(firstDate[1]) - 1
        firstDay = int(firstDate[2])
        endMonth = int(endDate[1])
        endDay = (int(endDate[2]) + 6) - totalDays[int(endDate[1]) + 1]
    else:
        firstMonth = int(firstDate[1]) - 1
        firstDay = int(firstDate[2])
        endMonth = int(endDate[1]) - 1
        endDay = int(endDate[2]) + 6
    
    dateText.text = biweeklyText.format(weekNum, weekNum + 1,
                                        englishMonth[firstMonth],
                                        firstDay, englishMonth[endMonth],
                                        endDay, yearNum, frenchMonth[firstMonth],
                                        frenchMonth[endMonth])
    fnameOut = biweeklyOut.format(yearNum, weekNum, weekNum + 1)
 
# Date modifier for weekly maps
elif (splitFname[5] == "Week"):
    if (re.search('[a-zA-Z]', splitFname[6][0:2])):
        weekNum = int(splitFname[6][0:1])
    else:
        weekNum = int(splitFname[6][0:2])                                               # Extracts the week number from the image name
    date = str(iso_to_gregorian(yearNum, weekNum, 1)).split("-")                        # Calculates the Gregorian date and receives a string containing the
                                                                                        # date in format YYYY-MM-DD then splits the string into a list of the
                                                                                        # three date values

    monthNum = int(date[1])                                                             # Extracts month number from the list of date values (date)
    dayNum = int(date[2])                                                               # Extracts day number from the list of date values (date)

    dateText.text = weeklyText.format(weekNum, englishMonth[monthNum - 1],
                                      dayNum, dayNum + 6, yearNum, 
                                      frenchMonth[monthNum - 1],
                                      dayNum, dayNum + 6)
    fnameOut = weeklyOut.format(yearNum, weekNum)


mxd.save()                                                                              # Saves the template copy
print "Exporting PDF to {0}".format(os.path.join(out_dir, fnameOut))
arcpy.mapping.ExportToPDF(mxd, os.path.join(out_dir, fnameOut))                        # Exports map to PDF

raw_input("Done. Press enter to exit.")
