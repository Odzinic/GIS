import Tkinter
import tkFileDialog
import arcpy
import os

arcpy.CheckOutExtension('Spatial')                                                      # Verifies that the Spatial Analyst extension is activated
root = Tkinter.Tk()

'''Directories'''
main_dir = os.getcwd()
tiff_dir = tkFileDialog.askdirectory(parent=root, initialdir="/",
                                    title='Folder containing GeoTIFFS')
poly_dir = tkFileDialog.askdirectory(parent=root, initialdir="/",
                                    title='Folder containing polygon')


'''Constants'''
tiffList = os.path.join(main_dir, os.listdir(tiff_dir)) 
poly  = os.path.join(main_dir, os.listdir(poly_dir)[0])

table = arcpy.sa.ZonalStatisticsAsTable(poly, 'FID', tiffList[0], 'outTable.csv', 'NODATA', 'MEAN')