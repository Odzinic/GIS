import os
import urllib2
import urlparse
from datetime import datetime

currTime = datetime.now().strftime('%Y%m%d_%H_%M')
main_dir = r"C:\Users\dzinico\workspace\EnvCanada_Download"
os.mkdir(os.path.join(main_dir, "downloaded", currTime))
file_dir = os.path.join(main_dir, "downloaded", currTime)
tmp_dir = os.path.join(main_dir, "temp")



strURL = r"http://dd.weatheroffice.gc.ca/model_gem_regional/10km/grib2/"
subDir = [r'/00/000/', r'/06/000/', r'/12/000/', r'/18/000/']
try:
    fileName = ['SNOD_SFC_0', 'TSOIL_SFC_0', 'TSOIL_DBLL_100', 'SOILW_DBLY_10',
                'TMP_TGL_2', 'ICEC_SFC_0' ]
except OSError:
    pass
strHTML = os.path.join(tmp_dir, "files.htm")



for path in subDir:
    currURL = strURL + path
    
    URLLib =  urllib2.urlopen(currURL)
    print "opened {0}".format(currURL)

    #----- Write HTML request to HTM file -----
    fHTML = open(strHTML, "w")
    fHTML.write(URLLib.read())
    fHTML.close()

    #----- Read file by line -----
    fHTML = open(strHTML, "r")
    lstFile = fHTML.readlines()
    fHTML.close()

    lstGrib2_Files = []
    
    for data in fileName:
        
#----- Iterate through lines -----
        for strLine in lstFile:
            if (strLine.count(data) != 0):

    #----- Find start and end indexes per line -----
                intStart = strLine.find(".grib2\">")
                intSkip = len(".grib2\">")
                intEnd = strLine.find("</a>")

    #---- If file found in line... -----
                if intStart != -1 and intEnd != -1:

        #----- Append to list -----
                    lstGrib2_Files.append(path + strLine[(intStart + intSkip):intEnd])
#----- Download files -----
    for strFiles in lstGrib2_Files:

        print("Downloading " + strFiles + "...")

    #----- Open file via URL -----
        print urlparse.urljoin(strURL, strFiles[1:])
        grib2_file = urllib2.urlopen(urlparse.urljoin(strURL, strFiles[1:]))

        #----- Write binaries locally -----
        fgrib2 = open(os.path.join(file_dir, strFiles[strFiles.index('CMC'):]), "wb")
        fgrib2.write(grib2_file.read())
        fgrib2.close()

print("\nCompleted...")