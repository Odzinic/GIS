import arcpy
from arcpy import sa as arcs
import os

arcpy.CheckOutExtension('Spatial')                                                      # Verifies that the Spatial Analyst extension is activated
arcpy.env.overwriteOutput = True

''' Directories '''
main_dir = os.getcwd()                                                                  # Directory which the script is located in
image_dir = os.path.join(main_dir, "Image_Input")                                       # Image directory
mask_dir = os.path.join(main_dir, "Buffers")                                            # Mask/buffer directory
if not os.path.exists(os.path.join(main_dir, "Output")):                                # Check to see if output folder exists and creates one if not
    os.makedirs(os.path.join(main_dir, "Output"))
out_dir = os.path.join(main_dir, "Output")

''' Constants '''
masks = filter((lambda x: x.endswith(".shp")), os.listdir(mask_dir))                                                              # List that loads all files in the mask/buffer directory
img = os.path.join(image_dir, filter((lambda x: x.endswith(".tif")), os.listdir(image_dir))[0])
typeInput = None

typeInput = raw_input("What type")
print typeInput
if (typeInput == '1'):
    imgType = "natural"
elif(typeInput == '2'):
    imgType = "infrared"
    
for mask in masks:
    outFolder = mask.strip('.shp')
    outName = "{0}_{1}".format(mask.strip('.shp'), imgType)
    try:
        os.mkdir(os.path.join(out_dir, outFolder))
    except WindowsError:
        pass
    extractMask = arcs.ExtractByMask(img, os.path.join(mask_dir, mask))            # Uses Extract by Mask to clip the input image to each mask
    extractMask.save(os.path.join(out_dir, outFolder, "{0}.tif".format(outName)))    # Saves the clip as "(CLIP_NAME)_clipped.tif" in temp directory
    print "{0} saved".format(outName)    

