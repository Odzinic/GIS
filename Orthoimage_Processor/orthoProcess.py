import arcpy, os
from arcpy import sa as arcsa

arcpy.env.overwriteOutput = True

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Script arguments
# inputWS = arcpy.GetParameterAsText(0)
# maskShp = arcpy.GetParameterAsText(1)
# namefield = arcpy.GetParameterAsText(2)
# outputWS = arcpy.GetParameterAsText(3)
#filetype = arcpy.GetParameterAsText(2)

main = os.getcwd()
inputWS = os.path.join(main, "input")
inRaster = os.path.join(inputWS, "Untitled.tif")
maskShp = os.path.join(inputWS, "sample_field.shp")
namefield = "T_ID"
outputWS = os.path.join(main, "out")


# Constants
inputs = os.listdir(inputWS)
maskFldr = os.path.join(outputWS, "masks")
blockSizes = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]

if (not os.path.exists(maskFldr)):
    os.mkdir(maskFldr)
    #
    
arcpy.Split_analysis(maskShp, maskShp, namefield, maskFldr)
masks = filter((lambda x: x.endswith(".shp")), os.listdir(maskFldr))

for mask in masks:
    currMask = os.path.join(maskFldr, "{0}.shp".format(mask))
    plotDir = os.path.join(outputWS, "Plot {0}".format(mask.split('.')[0]))
    focalDir = os.path.join(plotDir, "focal statistics")
    blockDir = os.path.join(plotDir, "block statistics")
    resampDir = os.path.join(plotDir, "resample")
    clipRaster = os.path.join(plotDir, "clipped_raster.tif")
    convertDir = os.path.join(plotDir, "convert")
    os.mkdir(plotDir)
    os.mkdir(focalDir)
    os.mkdir(blockDir)
    os.mkdir(resampDir)
    os.mkdir(convertDir)
    
    arcsa.ExtractByMask(inRaster, currMask).save(clipRaster)
    arcpy.RasterToOtherFormat_conversion(clipRaster, convertDir, "GRID")
    
    for size in blockSizes:
        focalsizeDir = os.path.join(focalDir, "{0}_by_{0}".format(size))
        blocksizeDir = os.path.join(blockDir, "{0}_by_{0}".format(size))
        resampsizeDir = os.path.join(resampDir, "{0}_by_{0}".format(size))
        
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
    
    