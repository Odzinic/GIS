import arcpy, os
from arcpy import sa as arcsa

arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

#  Script parameters
inRaster = arcpy.GetParameterAsText(0)                                                          # Input raster
maskShp = arcpy.GetParameterAsText(1)                                                           # Input mask shapefile        
nameField = arcpy.GetParameterAsText(2)                                                         # Field from the mask that will be used to name the different study areas
outputWS = arcpy.GetParameterAsText(3)                                                          # Output folder
classesNum = arcpy.GetParameter(4)                                                              # Number of classes the image will be classified to
resampleSizes = arcpy.GetParameter(5)                                                           # The resampling sizes that the tool will run (can be a single value or multiple)
classSize = arcpy.GetParameter(6)                                                               # The minimum number of pixels that a class must have to be a seperate class
sampleInterval = arcpy.GetParameter(7)                                                          



# Constants
maskFldr = os.path.join(outputWS, "masks")                                                      # Folder that contains all the extracted masking shapefiles
blockSizes = []                                                                                 # List that contains all of the inputed resample sizes
checkMask = True


#=============================================
# Iterates through all of the inputed resample
# sizes and appends the values to the blockSize
# list
#=============================================
for num in resampleSizes.split(','):
    blockSizes.append(int(num))


#=====================================================
# Condition that checks if a mask was inputed
# and if true checks that the inputed name field
# is a string. If false, creates a new string field
# and copies the name field values as strings into the
# new field
#=====================================================
if (maskShp != ""):
    for field in arcpy.ListFields(maskShp):
        if (field.name == nameField):
            if not(field.type == 'String'):
                arcpy.AddField_management(maskShp, "T_ID", "TEXT")
                arcpy.CalculateField_management(maskShp, "T_ID", "!{0}!".format(nameField), "PYTHON")
                nameField = "T_ID"



#=================================================
# Condition that checks if a mask was inputed
# and if true checks if a folder to contain the
# mask fields exist. If false, creates the folder 
# and stores the masks in the folder
#=================================================               
if (maskShp != ""):                                                                             # Check if a mask was inputed
    if (not os.path.exists(maskFldr)):                                                          # Check if mask folder exists
        os.mkdir(maskFldr)                                                                      # Creates mask folder if folder doesn't exist
        
    arcpy.Split_analysis(maskShp, maskShp, nameField, maskFldr)                                 # Splits the mask polygons into separate shapefiles
    masks = filter((lambda x: x.endswith(".shp")), os.listdir(maskFldr))                        # Creates a list of all of the masks


#=============================================
# Condition that checks if a mask was inputed
# and if false, skips the masking process  
#=============================================  
elif (maskShp == ""):
    masks = ['0.']
    checkMask = False                                                                           # Sets the mask check to false which indicates the script
                                                                                                # will skip the masking process
    

#============================================
# Iterates through all of the mask shapefiles
# and runs process with the mask
#============================================
for mask in masks:
    # File input and output paths for the following processes
    currMask = os.path.join(maskFldr, "{0}.shp".format(mask.split('.')[0]))                     # File path to the current mask
    plotDir = os.path.join(outputWS, "Plot {0}".format(mask.split('.')[0]))                     # Fle path to the folder that will be creates 
                                                                                                # for the outputs of the process with current mask
    rasMask = os.path.join(maskFldr, "{0}.tif".format(mask.split('.')[0]))                      # File path for the output of a raster version of
                                                                                                # the current mask
    focalDir = os.path.join(plotDir, "focal statistics")                                        # File path for the folder that will contain the
                                                                                                # outputs of the Focal Statistics tool
    blockDir = os.path.join(plotDir, "block statistics")                                        # File path for the folder that will contain the
                                                                                                # outputs of the Block Statistics tool
    resampDir = os.path.join(plotDir, "resample")                                               # File path for the folder that will contain the
                                                                                                # outputs of the Resampling tool
    clipRaster = os.path.join(plotDir, "clipped_raster.tif")                                    # File path of the output from the masking of the input
                                                                                                # raster
    convertDir = os.path.join(plotDir, "convert")                                               # File path for the folder that will contain the extracted
                                                                                                # bands from the clipped raster
    classifDir = os.path.join(plotDir, "classification")                                        # File path for the folder that will contain the classified
                                                                                                # raster
    
    
    #================================================
    # Conditions that check if required folder exist.
    # If false, creates the folder
    #================================================
    if(not os.path.exists(plotDir)):
        os.mkdir(plotDir)
    if(not os.path.exists(focalDir)):
        os.mkdir(focalDir)
    if(not os.path.exists(blockDir)):
        os.mkdir(blockDir)
    if(not os.path.exists(resampDir)):
        os.mkdir(resampDir)
    if(not os.path.exists(classifDir)):
        os.mkdir(classifDir)
    if(not os.path.exists(convertDir)):
        os.mkdir(convertDir)
    
    
    
    if (checkMask):
        arcpy.PolygonToRaster_conversion(currMask, nameField, rasMask)                          # Converts the current mask from a polygon to a raster        
        arcpy.Clip_management(inRaster, "", clipRaster, currMask, 0, "ClippingGeometry",        # Clips the input raster to the mask extent
                              "MAINTAIN_EXTENT")
        arcpy.RasterToOtherFormat_conversion(clipRaster, convertDir, "GRID")                    # Converts the clipped raster to a GRID format
        
    else:
        arcpy.Raster(inRaster).save(clipRaster)
        arcpy.RasterToOtherFormat_conversion(clipRaster, convertDir, "GRID")
        
    for size in blockSizes:
        focalsizeDir = os.path.join(focalDir, "{0}_by_{0}".format(size))
        blocksizeDir = os.path.join(blockDir, "{0}_by_{0}".format(size))
        resampsizeDir = os.path.join(resampDir, "{0}_by_{0}".format(size))
        classsizeDir = os.path.join(classifDir, "{0}_by_{0}".format(size))
        classifOut = os.path.join(classsizeDir, "Plot{0}_class".format(mask.split('.')[0]))
        polyclassOut = os.path.join(classsizeDir, "Plot{0}_class_poly.shp".format(mask.split('.')[0]))
        
        
        # File paths to the extracted raster bands
        band1 = os.path.join(convertDir, "clipped_c1")
        band2 = os.path.join(convertDir, "clipped_c2")
        band3 = os.path.join(convertDir, "clipped_c3")
        
        # File paths for the results of focal statistics 
        focalBand1 = os.path.join(focalsizeDir, "band_1")
        focalBand2 = os.path.join(focalsizeDir, "band_2")
        focalBand3 = os.path.join(focalsizeDir, "band_3")
        
        # File paths for the results of block statistics
        blockBand1 = os.path.join(blocksizeDir, "band_1")
        blockBand2 = os.path.join(blocksizeDir, "band_2")
        blockBand3 = os.path.join(blocksizeDir, "band_3")
        
        # Files paths for the results of resampling
        resampBand1 = os.path.join(resampsizeDir, "band_1")
        resampBand2 = os.path.join(resampsizeDir, "band_2")
        resampBand3 = os.path.join(resampsizeDir, "band_3")
        
        # Make folders to store the outputs of the processes
        os.mkdir(focalsizeDir)
        os.mkdir(blocksizeDir)
        os.mkdir(resampsizeDir)
        os.mkdir(classsizeDir)
        
        nbr = arcsa.NbrRectangle(size, size, "CELL")
        arcsa.FocalStatistics(band1, nbr, "MEAN", "DATA").save(focalBand1)
        arcsa.FocalStatistics(band2, nbr, "MEAN", "DATA").save(focalBand2)
        arcsa.FocalStatistics(band3, nbr, "MEAN", "DATA").save(focalBand3)
        
        
        nbr = arcsa.NbrRectangle(2, 2, "CELL")
        arcsa.BlockStatistics(focalBand1, nbr, "MEAN", "DATA").save(blockBand1)
        arcsa.BlockStatistics(focalBand2, nbr, "MEAN", "DATA").save(blockBand2)
        arcsa.BlockStatistics(focalBand3, nbr, "MEAN", "DATA").save(blockBand3)
        
        arcpy.Resample_management(blockBand1, resampBand1, "2", "BILINEAR")
        arcpy.Resample_management(blockBand2, resampBand2, "2", "BILINEAR")
        arcpy.Resample_management(blockBand3, resampBand3, "2", "BILINEAR")
        
        
        arcsa.IsoClusterUnsupervisedClassification([resampBand1, resampBand2, resampBand3], classesNum, classSize, sampleInterval).save(classifOut)
        arcpy.RasterToPolygon_conversion(classifOut, polyclassOut)
    