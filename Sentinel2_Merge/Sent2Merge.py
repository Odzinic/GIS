# Sentinel 2 Merge

#import gdal
import os
import shutil
import zipfile
from sys import argv
import arcpy
from arcpy import env

arcpy.env.overwriteOutput = True

inputDir = argv[1]
outputDir = os.path.join(os.getcwd(), "output")

inputZips = filter(lambda x: x.endswith('.zip'), os.listdir(inputDir))
imageDates = []

# Checks if the output directory exists and creates a folder if not
if not os.path.exists(outputDir):
	
	os.mkdir(outputDir)
	
for zipFile in inputZips:
	
	# Extracts the date of imagery zips from filename (Sentinel-2 currently has date in 3rd index pos)
	zipDate = zipFile.split('_')[3][:8]
	
	# Adds all the imagery dates to a list of dates
	if (not zipDate in imageDates):
		
		imageDates.append(zipDate)
		
		

for date in imageDates:
	
	# Creates a folder for each date in the output folder
	dateDir = os.path.join(outputDir, date)
	
	if not os.path.exists(dateDir):
		os.mkdir(dateDir)
	
	# List containing all of the zip files for each date
	currdateZips = filter(lambda x: date in x, inputZips)
	
	for zip in currdateZips:
		zipPath = os.path.join(inputDir, zip)
		with zipfile.ZipFile(zipPath) as zipOpen:
			for name in zipOpen.namelist():
				if (name.endswith('.jp2')):
					filename = os.path.basename(name)
					shutil.copyfileobj(zipOpen.open(name), file(os.path.join(dateDir, filename), "wb"))
					
					cellSize = int(arcpy.GetRasterProperties_management(os.path.join(dateDir, filename), "CELLSIZEX").getOutput(0))
					
					if (cellSize != 10):
						
						arcpy.Resample_management(os.path.join(dateDir, filename), os.path.join(dateDir, filename[0:-4]+"_10"+".jp2"), "10 10", "CUBIC")
						
					

			