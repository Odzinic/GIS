import os, string, subprocess
import arcpy
from arcpy import sa as arcs

arcpy.CheckOutExtension('Spatial')

print r"Input Path to the Folder Which Contains Shapefiles"
path_shape = raw_input()

print r"Input Path to the folder which Contains Classified Images"
path_image = raw_input()

print r"Input Path to the working folder"
working = raw_input()

main_dir = os.getcwd()
path_shape = os.path.join(main_dir, "Shapefiles")

lisimages = os.listdir(path_image) 
lisshapes = os.listdir(path_shape)

clipimage = filter((lambda x:"ON" in x), lisimages) 
print os.path.join(path_image,clipimage[0])

clipshape = filter((lambda x:"ON" in x and x.endswith('.shp')), lisshapes) 
print os.path.join(path_image,clipshape[0])

TEST = arcs.ExtractByMask(clipimage,clipshape) 
