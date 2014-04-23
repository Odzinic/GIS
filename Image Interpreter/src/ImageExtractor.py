'''Imports'''
import numpy as np                                                                      # NumPy used for creating arrays 
import os
import time
from osgeo import gdal
from osgeo import gdalconst
import datetime

gdal.AllRegister()
dr = gdal.GetDriverByName("GTiff")

'''Directories'''
dir = os.getcwd();                                                                      # Directory of the script
fn = os.path.join(dir, "images")                                                        # Directory of the image folder
oput = os.path.join(dir, "output")
final = os.path.join(dir, "output", "result.tiff")                                      # Resulting image

if (os.path.exists(fn)):
    next
else:
    os.mkdir(fn)
if (os.path.exists(oput)):
    next
else:
    os.mkdir(oput)


'''Image variables'''
image_files = os.listdir(fn)                                                            # Your list of images
temp_image = gdal.Open(os.path.join(os.path.join(fn + "\{0}".format(image_files[0]))))  # Load the first image to find the information of timeseries
image_width = temp_image.RasterXSize                                                   # Image width in pixels
image_length = temp_image.RasterYSize                                                   # Image length in pixels
img_stack = np.empty((image_length, image_width, len(image_files)), np.dtype('f'))      # Create empty array for values, dtype should be set to 'f' for float
date = []
temp_image = None

print "This image is {0} by {1}".format(image_width, image_length)

for i, fname in enumerate(image_files):
    dateString = fname.split("_")[0]
    dateConv = datetime.datetime(int(dateString[0:4]),
                                 int(dateString[4:6]),
                                 int(dateString[6:])) - datetime.datetime(int(dateString[0:4]), 1, 1) 
                             
    date.append(int(str(dateConv)[0: str(dateConv).index("day")]))
    print date[i]

'''Loop that loads images into a stack'''
for i, fname in enumerate(image_files):
    img = gdal.Open(os.path.join(fn + ("\{0}".format(fname)))).ReadAsArray()            # Reads an image into an array
    print ("Read {0}. The image is {1} by {2}".format(fname, 
                                                      image_width, image_length))       # Prints confirmation that image was read and its dimensions
    

    
    img_stack[:, :, i] = img                                                            # Stores the image array into a stack
    img = None                                                                          # Clears the loaded array to reduce memory usage


for x in range(image_width):
    for y in range(image_length):
        print img_stack[x, y]

raw_input("Finished")