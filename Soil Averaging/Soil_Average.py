'''
Created by Omar Dzinic (Omar.Dzinic@agr.gc.ca)
April 23, 2014

'''


'''Imports'''
import Tkinter, tkFileDialog
import arcpy
import os
import xlwt

arcpy.env.overwriteOutput = True                                                        # Enables overwriting
arcpy.CheckOutExtension('Spatial')                                                      # Verifies that the Spatial Analyst extension is activated
root = Tkinter.Tk()

'''Directories'''
main_dir = os.getcwd()
tiff_dir = tkFileDialog.askdirectory(parent=root, initialdir="/",                       # Select directory prompt for GeoTIFF folder
                                    title='Folder containing GeoTIFFS')
poly_dir = tkFileDialog.askdirectory(parent=root, initialdir="/",                       # Select directory prompt for polygon folder
                                    title='Folder containing polygon')

#tiff_dir = os.path.join(main_dir, 'tiff')
#poly_dir = os.path.join(main_dir, 'poly')

if not os.path.exists(os.path.join(main_dir, "output")):                                # Check to see if output folder exists and creates one if not
    os.makedirs(os.path.join(main_dir, "output"))
out_dir = os.path.join(main_dir, "output")                                              # Path for output directory


'''Constants'''
polyList = filter(lambda x: x.endswith('shp'), os.listdir(poly_dir))                    # Filters out all non .shp files in polygon folder
tiffList = os.listdir(tiff_dir)                                                         # Path for the folder of GeoTIFFS
poly  = os.path.join(main_dir, poly_dir, polyList[0])                                   # Path for input polygon

excel = os.path.join(out_dir, "Results.csv")                                            # Output path for results
book = xlwt.Workbook()                                                                  # Creates an Excel workbook
sh = book.add_sheet("Sheet")                                                            # Sheet for Excel workbook
bold = xlwt.easyxf('font: bold True;')                                                  # Font for the headers

allResults = []                                                                         # List that contains the results of the zonal statistic
  
i = 1
q = 0


'''Run Zonal Statistic on all TIFFs'''
# Performs a Zonal Statistic As Table mean operation 
# on every tiff in the tiff folder and saves it as a 
# .dbf. Also writes a header at the top of the excel
# for every tiff

# NOTE: The Zonal Statistic As Table operation skips over
# areas with NoData values and will result in a loss of 
# result for those polygons

for tiff in tiffList:                                                                   # Iterates through all of the tiffs in the tiff folder
    tiffPath = os.path.join(tiff_dir, tiff)                                             # Creates a path for every tiff in the iteration
    outPath = os.path.join(out_dir, "result{0}.dbf".format(i))                          # Creates a path for the output .dbfs
    table = arcpy.sa.ZonalStatisticsAsTable(poly, 'FID',                                # Runs Zonal Statistic As Table operation for input polygon
                                            tiffPath, outPath, 'DATA', 'MEAN')          # and tiff
    
    sh.write(0, i, tiff, bold)                                                          # Writes a header for the current tiff in the iteration    
    i += 1                                                                              # Constant used for the horizontal position of the header

tempout = filter(lambda x: x.endswith('.dbf'), os.listdir(out_dir))                     # Filters the output folder to remove any non-dbf files


'''Extract mean information from output tables'''
# Iterates through all of the .dbf tables and extracts
# the values from the mean field then appends it to a
# list (allResults)

for res in tempout:                                                                     # Iterates through all of the .dbf files in the output folder                                                          
    resultPath = os.path.join(out_dir, res)                                             # Creates a path for every dbf in the iteration
    fieldCursor = arcpy.SearchCursor(resultPath)                                        # Creates a SearchCursor for each dbf to allow for field extraction
    
    meanField = arcpy.ListFields(resultPath, "MEAN")[0]                                 # Extracts the mean field from the dbf table
    allResults.append([])                                                               
    
    for row in fieldCursor:                                                             # Iterates through all of the rows in the mean field
        allResults[q].append(row.getValue(meanField.name))                              # Appends the values at each row in the mean field to
                                                                                        # the list that contains the results (allResults)
    
    q += 1


'''Creates headers for polygon FIDs'''        
q = 1
for n in range(len(allResults[0])):
    sh.write(q, 0, n, bold)
    q += 1

q = 1
for values in allResults:
    i = allResults.index(values) + 1                                                    # Could cause crash if there are multiple exact same values
    for val in values:
        sh.write(q, i, val)
        q += 1
    q = 1
    

book.save(excel)                                                                        # Saves the Excel workbook as a .csv file