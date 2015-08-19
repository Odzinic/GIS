import arcpy, os
from arcpy import sa as arcsa

arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

#  Script arguments
inRaster = arcpy.GetParameterAsText(0)                                                          # Input raster
maskShp = arcpy.GetParameterAsText(1)                                                           # Input mask shapefile        
nameField = arcpy.GetParameterAsText(2)                                                         # Field from the mask that will be used to name the different study areas
outputWS = arcpy.GetParameterAsText(3)                                                          # Output folder
classesNum = arcpy.GetParameter(4)                                                              # 
resampleSizes = arcpy.GetParameter(5)
classSize = arcpy.GetParameter(6)
sampleInterval = arcpy.GetParameter(7)
# arcpy.AddMessage(classesNum)
# arcpy.AddMessage(type(classesNum))


# Constants
maskFldr = os.path.join(outputWS, "masks")
blockSizes = []
# blockSizes = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
checkMask = True

for num in resampleSizes.split(','):
    blockSizes.append(int(num))

if (maskShp != ""):
    for field in arcpy.ListFields(maskShp):
        if (field.name == nameField):
            if not(field.type == 'String'):
                arcpy.AddField_management(maskShp, "T_ID", "TEXT")
                arcpy.CalculateField_management(maskShp, "T_ID", "!{0}!".format(nameField), "PYTHON")
                nameField = "T_ID"
                
if (maskShp != ""):
    if (not os.path.exists(maskFldr)):
        os.mkdir(maskFldr)
        
    arcpy.Split_analysis(maskShp, maskShp, nameField, maskFldr)
    masks = filter((lambda x: x.endswith(".shp")), os.listdir(maskFldr))
    
elif (maskShp == ""):
    masks = ['0.']
    checkMask = False

for mask in masks:
    currMask = os.path.join(maskFldr, "{0}.shp".format(mask.split('.')[0]))
    plotDir = os.path.join(outputWS, "Plot {0}".format(mask.split('.')[0]))
    rasMask = os.path.join(maskFldr, "{0}.tif".format(mask.split('.')[0]))
    focalDir = os.path.join(plotDir, "focal statistics")
    blockDir = os.path.join(plotDir, "block statistics")
    resampDir = os.path.join(plotDir, "resample")
    clipRaster = os.path.join(plotDir, "clipped_raster.tif")
    convertDir = os.path.join(plotDir, "convert")
    classifDir = os.path.join(plotDir, "classification")
    
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
        arcpy.PolygonToRaster_conversion(currMask, nameField, rasMask)
#         arcsa.ExtractByMask(inRaster, rasMask).save(clipRaster)
        arcpy.Clip_management(inRaster, "", clipRaster, currMask, 0, "ClippingGeometry", "MAINTAIN_EXTENT")
        arcpy.RasterToOtherFormat_conversion(clipRaster, convertDir, "GRID")
        
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
        
        band1 = os.path.join(convertDir, "clipped_c1")
        band2 = os.path.join(convertDir, "clipped_c2")
        band3 = os.path.join(convertDir, "clipped_c3")
        
        focalBand1 = os.path.join(focalsizeDir, "band_1")
        focalBand2 = os.path.join(focalsizeDir, "band_2")
        focalBand3 = os.path.join(focalsizeDir, "band_3")
        
        blockBand1 = os.path.join(blocksizeDir, "band_1")
        blockBand2 = os.path.join(blocksizeDir, "band_2")
        blockBand3 = os.path.join(blocksizeDir, "band_3")
        
        resampBand1 = os.path.join(resampsizeDir, "band_1")
        resampBand2 = os.path.join(resampsizeDir, "band_2")
        resampBand3 = os.path.join(resampsizeDir, "band_3")
        
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
    