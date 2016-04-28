import os
import urllib
import urllib.request
import xlwt
from datetime import  datetime, timedelta

output_dir = r"C:\Users\DZINICOM\Downloads"
text_output = r"C:\Users\DZINICOM\Downloads\FireBlight_Conditions.xls"
bkp_fldr = os.path.join(output_dir, "FireBlight_Script_Bk")
sevenday_bkp = os.path.join(bkp_fldr, "7 Day Forecasts")
singleday_bkp = os.path.join(bkp_fldr, "24 Hour Forecasts")


temp_array = []
pop_array = []
precip_array = []
currTemp_array = []
currPop_array = []
currPrecip_array = []
counter = 0
temp_pos = 0
curr_pos = 0


locations = ["Alliston Simcoe South", "Bancroft - Hastings North", "Barrie Simcoe Central", "Barry's Bay - Renfrew West", 
             "Belle River- Essex North", "Belleville Hastings East", "Brant", "Britt", "Brockville Leeds and Grenville East",
             "Chatham- Kent West", "Coboconk - Victoria North", "Cobourg Northumberland West", "Collingwood Simcoe West", 
             "Cornwall Stormont, Dundas and Glengarry East", "Durham North", "Durham South", "Frontenac and LA central",
             "Frontenac and LA North", "Gananoque Leeds and Grenville West", "Georgina Beaverton", "Goderich Huron West",
             "Grand Bend", "Gravenhurst - Muskoka South", "Guelph Wellington South", "Haldimand Norfolk East", 
             "Haldimand Norfolk West", "Haliburton", "Halton North", "Halton South", "Hamilton", "Hamilton Wentworth North",
             "Hamilton Wentworth South", "Hawksbury Prescott and Russell East", "Huntsville - Muskoka North", "Kincardine Bruce West",
             "Kingston Frontenac South", "Leamington- Essex South", "Lindsay Victoria South", "Listowel Perth North",
             "London Middlesex East", "Long Point", "Madoc Hastings Central", "Manitoulin East", "Manitoulin West", 
             "Markdale Grey South", "Midland - Simcoe North", "Morrisburg Stormont, Dundas and Glengarry West",
             "Mount Forest Wellington North", "Napanee LA South", "Niagara East", "Niagara North", "Niagara South",
             "Niagara West", "Oil Springs Lambton South East", "Orangeville Dufferin", "Orillia - Simcoe North", "Ottawa Carleton",
             "Owen Sound Grey North", "Parry Sound", "Peel Central", "Peel North", "Peel South", "Pembroke - Renfrew North",
             "Perth Lanark South", "Peterborough North", "Peterborough South", "Picton Prince Edward", "Powassan",
             "Renfrew East - Lanark North", "Rockland Prescott and Russell West", "Sarnia Lambton NW", "St. Thomas Elgin",
             "Stratford Perth South", "Strathroy Middlesex West", "Sundridge - Burk's Falls", "Thamesville Kent East",
             "Tobermory - Bruce Penninsula North", "Toronto", "Trenton Hastings West Northumberland East", "Walkerton Bruce East",
             "Waterloo", "Wiarton Bruce Peninsula South", "Windsor-Essex West", "Wingham - Huron East", "Woodstock Oxford",
             "York North", "York South"]

url_code = {"Alliston Simcoe South": "so045", 
            "Bancroft - Hastings North": "so062", 
            "Barrie Simcoe Central": "so046", 
            "Barry's Bay - Renfrew West": "so078", 
            "Belle River- Essex North": "so003", 
            "Belleville Hastings East": "so060", 
            "Brant": "so016", 
            "Britt": "so085",
            "Brockville Leeds and Grenville East": "so068",
            "Chatham- Kent West": "so004",
            "Coboconk - Victoria North": "so054",
            "Cobourg Northumberland West": "so055",
            "Collingwood Simcoe West": "so047", 
            "Cornwall Stormont, Dundas and Glengarry East": "so071",
            "Durham North": "so051",
            "Durham South": "so050",
            "Frontenac and LA central": "so065",
            "Frontenac and LA North": "so066",
            "Gananoque Leeds and Grenville West": "so067",
            "Georgina Beaverton": "so052",
            "Goderich Huron West": "so024",
            "Grand Bend": "so008",
            "Gravenhurst - Muskoka South": "so075",
            "Guelph Wellington South": "so029",
            "Haldimand Norfolk East": "so015", 
            "Haldimand Norfolk West": "so014",
            "Haliburton":"so077",
            "Halton North": "so032",
            "Halton South": "so031",
            "Hamilton": "so019",
            "Hamilton Wentworth North": "so018",
            "Hamilton Wentworth South": "so017",
            "Hawksbury Prescott and Russell East": "so074",
            "Huntsville - Muskoka North": "so076",
            "Kincardine Bruce West": "so040",
            "Kingston Frontenac South": "so064",
            "Leamington- Essex South": "so002",
            "Lindsay Victoria South": "so053",
            "Listowel Perth North": "so027",
            "London Middlesex East": "so011",
            "Long Point": "so013",
            "Madoc Hastings Central": "so061",
            "Manitoulin East": "so082",
            "Manitoulin West": "so081", 
            "Markdale Grey South": "so043",
            "Midland - Simcoe North": "so048",
            "Morrisburg Stormont, Dundas and Glengarry West": "so070",
            "Mount Forest Wellington North": "so030",
            "Napanee LA South": "so063",
            "Niagara East": "so022",
            "Niagara North": "so023",
            "Niagara South": "so020",
            "Niagara West": "so021",
            "Oil Springs Lambton South East": "so006",
            "Orangeville Dufferin": "so036",
            "Orillia - Simcoe North": "so049",
            "Ottawa Carleton": "so072",
            "Owen Sound Grey North": "so044",
            "Parry Sound": "so083",
            "Peel Central": "so034",
            "Peel North": "so035",
            "Peel South": "so033",
            "Pembroke - Renfrew North": "so080",
            "Perth Lanark South": "so069",
            "Peterborough North": "so057",
            "Peterborough South": "so056",
            "Picton Prince Edward": "so058",
            "Powassan":"so086",
            "Renfrew East - Lanark North": "so079",
            "Rockland Prescott and Russell West": "so073",
            "Sarnia Lambton NW": "so007",
            "St. Thomas Elgin": "so009",
            "Stratford Perth South": "so026",
            "Strathroy Middlesex West": "so010",
            "Sundridge - Burk's Falls":"so084",
            "Thamesville Kent East": "so005",
            "Tobermory - Bruce Penninsula North": "so042",
            "Toronto": "so088",
            "Trenton Hastings West Northumberland East": "so059",
            "Walkerton Bruce East": "so039",
            "Waterloo": "so028",
            "Wiarton Bruce Peninsula South": "so041",
            "Windsor-Essex West": "so001",
            "Wingham - Huron East": "so025",
            "Woodstock Oxford": "so012",
            "York North": "so038",
            "York South": "so037"}

if (os.path.exists(bkp_fldr) == False):
        os.mkdir(bkp_fldr)
        
if (os.path.exists(sevenday_bkp) == False):
        os.mkdir(sevenday_bkp)
        
if (os.path.exists(singleday_bkp) == False):
        os.mkdir(singleday_bkp)


#===============================================================================
#                     Create a list of the dates of the week
#===============================================================================
weekDates = []                                                                  # Contains the 7 dates

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta
        
for result in perdelta(datetime.now(), 
                       datetime.now() + timedelta(days=7), timedelta(days=1)):
    weekDates.append(result.date())


wb = xlwt.Workbook(encoding="utf-8")
ws = wb.add_sheet("Temperatures")
ws.write(0, 0, "FarmZone")
ws.write(0, 1, "Date")
ws.write(0, 2, "Temperature")
ws.write(0, 3, "Precipitation")
dateStyle = xlwt.easyxf(num_format_str='MM/D/YY')


y_pos = 1


proxy_support = urllib.request.ProxyHandler({"http":"206.177.43.90:3128"})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)




 
for loc in locations:
    
    locCode = url_code[loc]
    sock = urllib.request.urlopen("http://www.farmzone.com/sevenday_forecast/{0}".format(locCode))
        
    siteHTML = sock.read()
    sock.close()
    
    save_path = os.path.join(sevenday_bkp, "{0}".format(datetime.now().date()))
    
    if (os.path.exists(save_path)):
        backup_file = open(os.path.join(save_path, "{0}.html".format(loc)), 'wb')
        backup_file.write(siteHTML)
        backup_file.close()
        
        
    else:
        os.mkdir(save_path)
        backup_file = open(os.path.join(save_path, "{0}.html".format(loc)), 'wb')
        backup_file.write(siteHTML)
        backup_file.close()
        
   
    print (loc)   
#     for url in siteHTML.split("\n"):
#         counter += 1
#         if 'daypop' in url:
#             counter += 5
#             rest = siteHTML.split("\n")[counter:]
#             for num in range(6):
#                 pop = rest[num].split('<td>')[1][:2]
#                 try:
#                     int(pop)
#                     pop_array.append(int(pop))
#                 except ValueError:
#                     pop_array.append(int(pop[:1]))
#             counter = 0
#             break
  
          
    for url in siteHTML.split(b"\n"):
        counter += 1    
        if b'High Temperature' in url:
            counter += 1
            rest = siteHTML.split(b"\n")[counter:]
            for num in range(6):
                temp = rest[num].split(b'<td>')[1][:2]
                try:
                    int(temp)
                    temp_array.append(int(temp))
                except ValueError:
                    temp_array.append(int(temp[:1]))
            counter = 0
            break
          
    for url in siteHTML.split(b"\n"):
        counter += 1    
        if b'<h2 class="alt">Rain</h2>' in url:
            counter += 1
            rest = siteHTML.split(b"\n")[counter:]
            for num in range(6):
                temp = rest[num].split(b'<td>')[1]
                if (temp == b'-</td>\r'):
                    precip_array.append(0)
                     
                elif (b'less than 1' in temp):
                    precip_array.append(1)  
                       
                elif(b'close to ' in temp):
                    try:
                        int(temp[9:11])
                        precip_array.append(int(temp[9:11]))
                    except ValueError:
                        precip_array.append(int(temp[9:10]))
                         
                elif(len(temp.split(b'-')) == 2):
                    try:
                        int(temp.split(b'-')[1][:2])
                        precip_array.append(int(temp.split(b'-')[1][:2]))
                    except ValueError:    
                        precip_array.append(int(temp.split(b'-')[1][:1]))
                
                else:
                    print ("broken", temp)      
            counter = 0
            break
        elif(len(siteHTML.split(b"\n")) == counter):
            for num in range(6):
                precip_array.append(0)
            counter = 0
            break
        
        
             
          
for loc in locations:
    locCode = url_code[loc]
    sock = urllib.request.urlopen("http://www.farmzone.com/next_twentyfourhours/{0}".format(locCode))
        
    siteHTML = sock.read()
    sock.close()
    
    save_path = os.path.join(singleday_bkp, "{0}".format(datetime.now().date()))
    
    if (os.path.exists(save_path)):
        backup_file = open(os.path.join(save_path, "{0}.html".format(loc)), 'wb')
        backup_file.write(siteHTML)
        backup_file.close()
        
        
    else:
        os.mkdir(save_path)
        backup_file = open(os.path.join(save_path, "{0}.html".format(loc)), 'wb')
        backup_file.write(siteHTML)
        backup_file.close()
     
    print (loc)
       
    for url in siteHTML.split(b"\n"):
        counter += 1
        if b'sttemp' in url:
            counter += 4
            rest = siteHTML.split(b"\n")[counter:]
            curr_temp = rest[0].split(b'<td class="temp">')[1][:2]
            try:
                int(curr_temp)
                currTemp_array.append(int(curr_temp))
            except ValueError:
                currTemp_array.append(int(curr_temp[:1]))   
            counter = 0
            break
         
    for url in siteHTML.split(b"\n"):
        counter += 1    
        if b'stprecip' in url:
            counter += 6
            rest = siteHTML.split(b"\n")[counter:]
            temp = rest[1]
            print (temp)
            if (b'\t-\t' in temp):
                currPrecip_array.append(0)
                  
            elif (b'close to 1mm' in temp or b'less than 1mm' in temp):
                currPrecip_array.append(1)  
                    
            elif(b'close to' in temp):
                try:
                    int(temp[temp.index(b'to')+2 : temp.index(b'to')+5])
                    currPrecip_array.append(int(temp[temp.index(b'to')+2 : temp.index(b'to')+5]))
                except ValueError:
                    currPrecip_array.append(int(temp[temp.index(b'to')+2 : temp.index(b'to')+4]))
                      
            elif(len(temp.split(b'-')) == 2):
                try:
                    int(temp[temp.index(b'-') + 1: temp.index(b'-') + 3])
                    currPrecip_array.append(int(temp[temp.index(b'-') + 1: temp.index(b'-') + 3]))
                except ValueError:    
                    currPrecip_array.append(int(temp[temp.index(b'-') + 1: temp.index(b'-') + 2]))
                                
            counter = 0
            break
        elif(len(siteHTML.split(b"\n")) == counter):
            counter = 0
            currPrecip_array.append(0)
            break
           
#     for url in siteHTML.split("\n"):
#         counter += 1
#         if 'stpop' in url:
#             counter += 5
#             rest = siteHTML.split("\n")[counter:]
#             pop = rest[0].split('<td>')[1][:2]
#             try:
#                 int(pop)
#                 currPop_array.append(int(pop))
#             except ValueError:
#                 currPop_array.append(int(pop[:1]))
#             counter = 0
#             break
 
     
          
    for num in range(7):
        if (num == 0):
            ws.write(y_pos, 0, loc)
            ws.write(y_pos, 1, weekDates[num], dateStyle)
            ws.write(y_pos, 2, currTemp_array[curr_pos])
            ws.write(y_pos, 3, currPrecip_array[curr_pos])
            y_pos += 1
        else:
            ws.write(y_pos, 0, loc)
            ws.write(y_pos, 1, weekDates[num], dateStyle)
            ws.write(y_pos, 2, temp_array[temp_pos])
            ws.write(y_pos, 3, precip_array[temp_pos])
            y_pos += 1
            temp_pos += 1
            wb.save(text_output)
#             print "{0} written".format(loc)
         
    curr_pos += 1
        
wb.save(text_output)
     

