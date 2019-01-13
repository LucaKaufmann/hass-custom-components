import csv
from pathlib import Path
from optparse import OptionParser
from math import radians, cos, sin, asin, sqrt
from datetime import datetime

parser = OptionParser()
parser.add_option("-t", "--lat", dest="latitude",
                  help="latitude", action="store", type="float")
parser.add_option("-o", "--long", dest="longitude",
                  help="longitude", action="store", type="float")
parser.add_option("-d", "--date", dest="date",
                  help="date", action="store", type="string")
parser.add_option("-p", "--person", dest="person",
                  help="person", action="store", type="string")

(options, args) = parser.parse_args()
latitude = options.latitude
longitude = options.longitude
date = options.date
person = options.person

today = datetime.today()
currentMonth = datetime.now().month
currentYear = datetime.now().year
date = str(currentYear)+"-"+str(currentMonth)

path = "/config/export/"+date+"-"+person+".csv"

values = Path(path)
if values.is_file():
    with open(path, 'a') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow([latitude,longitude,date])

else:
    with open(path,'w') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(['latitude','longitude','date'])
        newFileWriter.writerow([latitude,longitude,date])