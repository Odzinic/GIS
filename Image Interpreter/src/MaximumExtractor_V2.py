'''Imports'''
import numpy as np                                                                      # NumPy used for creating arrays 
import os
import time
from osgeo import gdal
from osgeo import gdalconst


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
max_img = gdal.Open(os.path.join(os.path.join(fn + "\{0}".format(image_files[0])))) # Load the first image to find the information of timeseries
print "Loaded"
image_width = max_img.RasterYSize                                                    # Image width in pixels
image_length = max_img.RasterXSize                                                   # Image length in pixels
geo_proj = max_img.GetProjectionRef()                                                # Contains all metadata contents
geo_tranf = max_img.GetGeoTransform()                                                   # List that holds the extracted 
print "Creating array"
img_stack = np.empty((image_width, image_length, 2), np.dtype('int16'))

total_time = 0.0

def timeReset():
    start_time = 0.0
    end_time = 0.0
    
max_img = max_img.ReadAsArray()  
  
for i, fname in enumerate(image_files):
    curr_img = gdal.Open(os.path.join(fn + ("\{0}".format(fname)))).ReadAsArray()            # Reads an image into an array
    print ("Read {0}. The image is {1} by {2}".format(fname, 
                                                      image_length, image_width))       # Prints confirmation that image was read and its dimensions
    img_stack[:, :, 0] = max_img                                                     # Stores the image array into a stack
    img_stack[:, :, 1] = curr_img
    max_img =  np.amax(img_stack, 2)
    
output_raster = dr.Create(final, image_length, image_width, 1, gdal.GDT_Float32)
output_raster.GetRasterBand(1).WriteArray(max_img)
output_raster.SetProjection(geo_proj)
output_raster.SetGeoTransform(geo_tranf)
    
print max_img
    