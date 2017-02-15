import os
import shutil
import arcpy
from arcpy import env

arcpy.env.overwriteOutput = True

inputDir = argv[1]
outputDir = os.path.join(os.getcwd(), "merged")

# Dictionary containing the ending of the filenames for each band
bandDic = {"Band_1": "B01_10.jp2",
	   "Band_2": "B02.jp2",
	   "Band_3": "B03.jp2",
	   "Band_4": "B04.jp2",
	   "Band_5": "B05_10.jp2",
	   "Band_6": "B06_10.jp2",
	   "Band_7": "B07_10.jp2",
	   "Band_8": "B08.jp2",
	   "Band_8A": "B08A_10.jp2",
	   "Band_9": "B09_10.jp2",
	   "Band_10": "B10_10.jp2",
	   "Band_11": "B11_10.jp2",
	   "Band_12": "B12_10.jp2",
	   "Band_PVI": "PVI_10.jp2",
	   "Band_TCI": "TCI.jp2"}
	   	
}
