# -*- coding: utf-8 -*-

import arcpy 
import arcpy.mapping as arcm
from arcpy import env
import os
from shutil import copyfile
import datetime
import env



'''Directories'''
main_dir = os.getcwd() # Directory of script
img_dir = os.path.join(main_dir, "Input_Image")
template_dir = os.path.join(main_dir, "Input_Template")
vector_dir = os.path.join(main_dir, "Input_Vectors")

if not os.path.exists(os.path.join(main_dir, "Output")):
    os.makedirs(os.path.join(main_dir, "Output"))
out_dir = os.path.join(main_dir, "Output")




'''Constants'''
in_img = os.listdir(img_dir)[0]
print "Input image is {0}".format(in_img)

in_template = os.listdir(template_dir)[0]
print "Input template is {0}".format(in_template)

copyfile(os.path.join(template_dir, in_template), os.path.join(out_dir, in_template))
mxd = arcpy.mapping.MapDocument(os.path.join(out_dir, in_template))

testDframe = arcm.ListDataFrames(mxd)[0]

projection = "PROJCS['North_America_Lambert_Conformal_Conic',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-96.0],PARAMETER['Standard_Parallel_1',20.0],PARAMETER['Standard_Parallel_2',60.0],PARAMETER['Latitude_Of_Origin',40.0],UNIT['Meter',1.0]]"
inproj = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"

input = "C:\\Users\\dzinico\\Documents\\Weekly Map Automator\\Weekly_Maps\\Input_Vectors\\GlobAv_SMUDP2_OPER_551_2013_Week_48WGS84.tif"
output = "C:\\Users\\dzinico\Documents\\Weekly Map Automator\\Weekly_Maps\\Input_Vectors\\temp.tif"

englishMonth = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
frenchMonth = ['janvier', 'f�vrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'ao�t', 'septembre', 'octobre', 'novembre', 'd�cembre']




'''Reproject tiff'''
#if os.path.exists(output):
#    os.remove(output)
#
reprojTif = filter(lambda x: str(x).endswith(".tif"), arcm.ListLayers(mxd))[0]
fname = str(reprojTif)
#
#arcpy.ProjectRaster_management(input, output, projection, "", "28000", "NAD_1983_To_WGS_1984_1", "", inproj)
#
#os.remove(input)
#os.rename(output, input)




'''Set data paths'''
#for lyr in arcm.ListLayers(mxd):
#    name = str(lyr)
#    print lyr.dataSource
#    arcm.RemoveLayer(testDframe, lyr)
#    if ((lyr.dataSource).endswith(".tif")):
#        lyr.replaceDataSource(vector_dir, "RASTER_WORKSPACE", name)
#    else:
#        lyr.replaceDataSource(vector_dir, "SHAPEFILE_WORKSPACE", name)
#    arcm.AddLayer(testDframe, lyr, "AUTO_ARRANGE")
#    print lyr.dataSource
#    
#    
#    
#    
#
#mxd.save()
#
#
#arcpy.mapping.ExportToPDF(mxd, r"C:\Users\dzinico\Documents\Weekly Map Automator\Weekly_Maps\Output\Map.pdf")




'''Change the week number and date'''


def iso_year_start(iso_year):
    "The gregorian calendar date of the first day of the given ISO year"
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta 

def iso_to_gregorian(iso_year, iso_week, iso_day):
    "Gregorian calendar date for the given ISO year, week and day"
    year_start = iso_year_start(iso_year)
    return year_start + datetime.timedelta(days=iso_day-1, weeks=iso_week-1)

date = str(iso_to_gregorian(2013, 23, 2)).split("-")
yearNum = int(date[0])
monthNum = int(date[1])
dayNum = int(date[2])
weekNum = fname.split("_")[6][0:2]

print yearNum
print monthNum
print dayNum
print weekNum

for txt in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
    if txt.name == "Week Info":
        txt.text = "Week {0} ({1} {2} - {1} {3}), {4} / Sesmaine {0} ({5} {6} au {7} {6}), {4}".format(weekNum, englishMonth[monthNum - 1], dayNum, dayNum + 6, yearNum, frenchMonth[monthNum - 1], dayNum, dayNum + 6)

mxd.save()