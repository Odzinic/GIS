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

projection = "PROJCS['North_America_Lambert_Conformal_Conic',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-96.0],PARAMETER['Standard_Parallel_1',20.0],PARAMETER['Standard_Parallel_2',60.0],PARAMETER['Latitude_Of_Origin',40.0],UNIT['Meter',1.0]]"
inproj = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"

tiffInput = os.path.join(img_dir, str(os.listdir(img_dir)[0]))                          # The input tiff image
tiffOutput = os.path.join(vector_dir, "temp.tif")                                       # The path to the temp copy of the tiff image


englishMonth = ['January', 'February', 'March', 'April', 'May', 'June', 'July',         # List of months
                'August', 'September', 'October', 'November', 'December']               # in English for date
                                                                                                                                          
frenchMonth = ['janvier', 'f�vrier', 'mars', 'avril', 'mai', 'juin', 'juillet',          # List of months
               'ao�t', 'septembre', 'octobre', 'novembre', 'd�cembre']                   # in French for date




copyfile(tiffInput, tiffOutput)                                                         # Create temp of the tiff image and put it in vectors directory



'''Reproject tiff'''
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

def iso_year_start(iso_year):                                                           # The Gregorian calendar date of the first day of the given ISO year
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday() - 1)
    return fourth_jan - delta 

def iso_to_gregorian(iso_year, iso_week, iso_day):                                      # Gregorian calendar date for the given ISO year, week and day
    year_start = iso_year_start(iso_year)
    return year_start + datetime.timedelta(days=iso_day - 1, weeks=iso_week - 1)

weekNum = int(fname.split("_")[6][0:2])                                                 # Extracts the week number from the image name
yearNum = int(fname.split("_")[4])                                                      # Extracts the year number from the image name

date = str(iso_to_gregorian(yearNum, weekNum, 1)).split("-")                            # Calculates the Gregorian date and receives a string containing the
                                                                                        # date in format YYYY-MM-DD then splits the string into a list of the
                                                                                        # three date values

monthNum = int(date[1])                                                                 # Extracts month number from the list of date values (date)
dayNum = int(date[2])                                                                   # Extracts day number from the list of date values (date)



for txt in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
    if txt.name == "Week Info":
        txt.text = "Week {0} ({1} {2} - {1} {3}), {4} / Semaine {0} ({5} {6} au {5} {7}), {4}".format(weekNum, englishMonth[monthNum - 1],
                                                                                                       dayNum, dayNum + 6, yearNum, frenchMonth[monthNum - 1],
                                                                                                       dayNum, dayNum + 6)

mxd.save()                                                                              # Saves the template copy
print "Exporting PDF to {0}".format(os.path.join(out_dir, "Map.pdf"))
arcpy.mapping.ExportToPDF(mxd, os.path.join(out_dir, "Map.pdf"))                        # Exports map to PDF

raw_input("Done. Press enter to exit.")
