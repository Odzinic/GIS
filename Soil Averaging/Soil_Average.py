import Tkinter, tkFileDialog
import arcpy
import os
import xlwt

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension('Spatial')                                                      # Verifies that the Spatial Analyst extension is activated
root = Tkinter.Tk()

'''Directories'''
main_dir = os.getcwd()
#tiff_dir = tkFileDialog.askdirectory(parent=root, initialdir="/",
#                                    title='Folder containing GeoTIFFS')
#poly_dir = tkFileDialog.askdirectory(parent=root, initialdir="/",
#                                    title='Folder containing polygon')

tiff_dir = os.path.join(main_dir, 'tiff')
poly_dir = os.path.join(main_dir, 'poly')

if not os.path.exists(os.path.join(main_dir, "output")):                                # Check to see if output folder exists and creates one if not
    os.makedirs(os.path.join(main_dir, "output"))
out_dir = os.path.join(main_dir, "output")


'''Constants'''
polyList = filter(lambda x: x.endswith('shp'), os.listdir(poly_dir))
tiffList = os.listdir(tiff_dir)
poly  = os.path.join(main_dir, poly_dir, polyList[0])

excel = os.path.join(out_dir, "Results.csv")
book = xlwt.Workbook()                                                                  # Creates an Excel workbook
sh = book.add_sheet("Sheet")  
bold = xlwt.easyxf('font: bold True;')

allResults = []
  
i = 1
q = 0

for tiff in tiffList:
    tiffPath = os.path.join(tiff_dir, tiff)
    outPath = os.path.join(out_dir, "result{0}.dbf".format(i))
    table = arcpy.sa.ZonalStatisticsAsTable(poly, 'FID', tiffPath, outPath, 'DATA', 'MEAN')
    sh.write(0, i, tiff, bold)
    i += 1

tempout = filter(lambda x: x.endswith('.dbf'), os.listdir(out_dir))

for res in tempout:
    resultPath = os.path.join(out_dir, res)
    fieldCursor = arcpy.SearchCursor(resultPath)
    
    meanField = arcpy.ListFields(resultPath, "MEAN")[0]
    allResults.append([])
    
    for row in fieldCursor:
        allResults[q].append(row.getValue(meanField.name))
    
    q += 1
        
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
    

book.save(excel) 