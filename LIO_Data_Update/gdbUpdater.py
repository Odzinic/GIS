import os
import shutil
import zipfile
import arcpy
import datetime

zipDir = r"J:\LIO_Data_Download"
firstextractDir = os.path.join(zipDir, "extract_data")
finalextractDir = os.path.join(zipDir, "final_data")
testDir = os.path.join(zipDir, "test_folder")
errorTxt = os.path.join(zipDir, "error_log.txt")
errorLog = []

zipFiles = filter((lambda x: x.endswith('.zip')), os.listdir(zipDir))

if (not os.path.isdir(firstextractDir)):
    os.mkdir(firstextractDir)
    
if (not os.path.isdir(finalextractDir)):
    os.mkdir(finalextractDir)
    

for zip in zipFiles:
    zipPath = os.path.join(zipDir, zip)
    zipFile = zipfile.ZipFile(zipPath)
      
    print "Extracting first zip file."
    zipFile.extractall(firstextractDir)
    zipFile.close()
    print "Extracted first zip file."
       
    finalZip = filter((lambda x: x.endswith('.zip')), os.listdir(firstextractDir))[0]
    finalzipPath = os.path.join(firstextractDir, finalZip)
    finalzipFile = zipfile.ZipFile(finalzipPath)
    print "Extracting GDB from zip file."
    finalzipFile.extractall(finalextractDir)
    finalzipFile.close()
    print "Extracted GDB"
       
    gdbName = finalZip.strip('.zip').split('-')[-1]
    print "Renaming extracted GDB to {0}.".format(gdbName)
    os.rename(os.path.join(finalextractDir, "Non_Sensitive.gdb"), os.path.join(finalextractDir, "{0}_Non_Sensitive.gdb".format(gdbName)))
    print "Removing temporary files." 
    os.remove(finalzipPath)
  
     
gdbDir = filter((lambda x: x.endswith('.gdb')), os.listdir(finalextractDir))

for gdb in gdbDir:
    currGDB = os.path.join(finalextractDir, gdb)
    outGDB = os.path.join(testDir, gdb)
    
    if os.path.isdir(outGDB):
        print "The GDB destination exists at path {0}. Deleting old GDB.".format(outGDB)
        try:
            arcpy.Delete_management(outGDB)
            print "Copying new GDB to destination path."
            shutil.copytree(currGDB, outGDB)
        except arcpy.ExecuteError:
            errorLog.append("Unable to update {0}. May be due to a lock from an application.".format(gdb))
            
if (errorLog != []):
    errorFile = file(errorTxt, 'w')
    for error in errorLog:
        errorFile.write("({0}) {1}\n".format(datetime.datetime.now().time(), error))
    errorFile.close()
    

    

