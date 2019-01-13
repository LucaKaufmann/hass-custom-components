from gmplot import gmplot
import csv
from optparse import OptionParser
from math import radians, cos, sin, asin, sqrt
from datetime import datetime

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


parser = OptionParser()
parser.add_option("-p", "--person", dest="person",
                  help="person", action="store", type="string")

(options, args) = parser.parse_args()
person = options.person

# Place map

# gmap = gmplot.GoogleMapPlotter(12.3456789, 12.3456789, 10)
gmap = gmplot.GoogleMapPlotter(12.3456789, 12.3456789, 9, "API_KEY")

today = datetime.today()
currentMonth = datetime.now().month
currentYear = datetime.now().year
date = str(currentYear)+"-"+str(currentMonth)

path = "/config/export/"+date+"-"+person+".csv"

gps = []
with open(path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    line_count = 0
    previous_row = []
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            if previous_row:
                prev_lat = float(previous_row[0])
                prev_lon = float(previous_row[1])
                lat = float(row[0])
                lon = float(row[1])
                a = haversine(float(prev_lat), float(prev_lon), float(lat), float(lon))
                radius = 0.05
                # print('Distance (km) : ', a)
                if a <= radius:
                    continue
                else:
                    gps.append((lat,lon))
                    previous_row = row
            else:
                gps.append((float(row[0]),float(row[1])))
                previous_row = row
            
# Polygon
lats, lons = zip(*gps)

color = 'cornflowerblue'

if person == 'luca':
	color = 'orange'
elif person == 'tiia':
	color = 'purple'


gmap.plot(lats, lons, color, edge_width=5)

gmap.draw("/config/www/"+person+"_gps.html")