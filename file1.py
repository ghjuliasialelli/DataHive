# XML PARSING 
import xml.etree.ElementTree as PARSER
# Percent encoding
import urllib.parse
# For HTTP requests
import requests

API_KEY = "AIzaSyDSlnWcTV2bIenN_JTnn6BzLNeBI0tHOtA"

# input : [(hotelname, ....) ,..]
# extract hotel names
#input = [...]
locations = ["Rue Jacques Brel Espace de L'Archer 02200", "RUE DU MOULIN LE BLANC 08000", "ZAC L'écluse des Marots - Parc Sud Saint Thibaud	10800"]
        #locations = [input[i][Hotel.address] for i in range(len(input))]


# Lauch the Google maps API
base_url= "https://maps.googleapis.com/maps/api/distancematrix/xml" # pas de '?' a la fin en utilisant requests 

origins = urllib.parse.quote_plus(locations[0])
for i in range(1, len(locations)):
    origins = origins+"|"+urllib.parse.quote_plus(locations[i])

# Step 1 : construct the URL for driving
# example : https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&key=YOUR_API_KEY
params_driving = {'origins':origins, 'destinations':origins, 'key':API_KEY}
        #base_url_driving = base_url + "origins=" + origins + "&destinations=" + origins + "&key=" + API_KEY
r_driving = requests.get(base_url, params=params_driving)
data_driving = r_driving.text

# Step 2 : construct the URL for transit 
params_transit = {'origins':origins, 'destinations':origins, 'mode':'transit', 'key':API_KEY}
        #base_url_driving = base_url + "origins=" + origins + "&destinations=" + origins + "mode=transit" + "&key=" + API_KEY
r_transit = requests.get(base_url, params=params_transit)
data_transit = r_transit.text


# Parse input XML for driving 
root_driving = PARSER.fromstring(data_driving)
driving_matrix = [[0 for _ in range(len(locations))] for _ in range(len(locations))]

print(data_driving)

print("len location", len(locations))

i=0
for row in root_driving.getiterator("row"):
    j = 0
    for column in row.getiterator("element"):
        for duration in column.getiterator("duration"):
            for value in list(duration):
                if value.tag == "value": 
                    print("i,j", (i,j))
                    driving_matrix[i][j] = value.text 
        j+=1
    i+=1

# Parse input XML for transit 
root_transit = PARSER.fromstring(data_transit)
transit_matrix = [[0 for _ in range(len(locations))] for _ in range(len(locations))]

i=0
for row in root_transit.getiterator("row"):
    j=0
    for column in row.getiterator("element"):
        for duration in column.getiterator("duration"):
            for value in list(duration):
                if value.tag == "value": 
                    transit_matrix[i][j] = value.text 
        j+=1
    i+=1


print(driving_matrix)
print(transit_matrix)