'''Imports'''
import numpy as np # NumPy used for creating arrays 
import os
import time
from osgeo import gdal
from osgeo import gdalconst

gdal.AllRegister()
dr = gdal.GetDriverByName("GTiff")

'''Directories'''
dir = os.getcwd(); # Directory of the script
fn = os.path.join(dir, "images") # Directory of the image folder
oput = os.path.join(dir, "output")
final = os.path.join(dir, "output", "result.tiff") # Resulting image

if (os.path.exists(fn)):
    next
else:
    os.mkdir(fn)
if (os.path.exists(oput)):
    next
else:
    os.mkdir(oput)


'''Image variables'''
image_files = os.listdir(fn) # Your list of images
temp_image = gdal.Open(os.path.join(os.path.join(fn + "\{0}".format(image_files[0])))) # Load the first image to find the information of timeseries
image_width = temp_image.RasterYSize # Image width in pixels
image_length = temp_image.RasterXSize # Image length in pixels
geo_proj = temp_image.GetProjectionRef() # Contains all metadata contents
geo_tranf = temp_image.GetGeoTransform()
img_stack = np.empty((image_width, image_length, len(image_files)), np.dtype('f')) # Create empty array for values, dtype should be set to 'f' for float
final_values = {} # Dictionary that holds the extracted z values in format z = final_values[x_value][y_value]
min_values = {}
temp_image = None

total_time = 0.0




def timeReset():
    start_time = 0.0
    end_time = 0.0


'''Loop that loads images into a stack'''
for i, fname in enumerate(image_files):
    img = gdal.Open(os.path.join(fn + ("\{0}".format(fname)))).ReadAsArray() # Reads an image into an array
    print ("Read {0}. The image is {1} by {2}".format(fname, image_length, image_width)) # Prints confirmation that image was read and its dimensions
    img_stack[:, :, i] = img # Stores the image array into a stack
    img = None # Clears the loaded array to reduce memory usage
    
 
print ("Processing images")
start_time = time.time()

for x in range(image_length):
    final_values[x] = {}
    for y in range(image_width):
        final_values[x][y] = []
        for z in range(len(image_files)):
            final_values[x][y].append(img_stack[y, 0, z])
    img_stack = np.delete(img_stack, 0, 1)
end_time = time.time();

total_time = total_time + ((end_time - start_time) / 60.0)
print ("Processing took {0} minutes".format((end_time - start_time) / 60.0))
timeReset()


print ("Finding maximum values")
start_time = time.time()

#print ("Finding minimum values")
#start_time = time.time()
#
#for x in range(image_length):
#    min_values[x] = {}
#    for y in range(image_width):
#        min_values[x][y] = min(final_values[x][y])
#
#end_time = time.time();
#
#total_time = total_time + ((end_time - start_time) / 60.0)
#print ("Finding minimum took {0} minutes".format((end_time - start_time) / 60.0))
#timeReset()

max_values = np.empty((image_width, image_length), np.dtype('f'))
output_raster = dr.Create(final, image_length, image_width , 1, gdal.GDT_Float32)##Changed

for x in range(image_width):
    for y in range(image_length):
        max_values[x][y] = max(final_values[y][x])
final_values =  None        
end_time = time.time();

total_time = total_time + ((end_time - start_time) / 60.0)
print ("Finding maximums took {0} minutes".format((end_time - start_time) / 60.0))
timeReset()


output_raster.GetRasterBand(1).WriteArray(max_values)
output_raster.SetProjection(geo_proj)
output_raster.SetGeoTransform(geo_tranf)

print ("Total processing time was {0} minutes".format(total_time))

prompt = input("Press enter to exit")



    
    
    
    
    
    
    
    
    
    
    
    



