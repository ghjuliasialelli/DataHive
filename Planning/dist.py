# XML PARSING 
import xml.etree.ElementTree as PARSER
# Percent encoding
import urllib.parse
# For HTTP requests
import requests
# For Haversinee formula
from math import cos, asin, sqrt


distance_dic = [{},{}]
# distance_dic[0] : distances by transit
# distance_dic[1] : distances by car

inputt =    [[225,"Grand Hôtel d'Aboukir", "134 rue d'Aboukir","75002", 35, 7], 
            [7180332, "Chaussée d'Antin", "46 rue de la Chaussée d'Antin", "75009", 34, 3],
            [3029096, "Métropolitain", "158 rue Oberkampf", "75011", 60, 5],
            [69, "Cristal","64 rue de la Jonquière","75017", 98, 10],
            [160, "des Beaux-Arts","4 rue André Antoine","75018", 76, 2],
            [14664544, "Moderne - Paris 20ème","57 rue de la Réunion","75020", 41,10],
            [7923060, "Sofiane","66 boulevard de Charonne","75020",47,2],
            [7877630, "Hipotel Paris Buttes Chaumont","7 rue Jean Baptiste Dumay","75020", 73,5],
            [130, "de Normandie", "4 rue d'Amsterdam","75009", 200,3],
            [5928342, "Maison Blanche","107 Bis Avenue d'Italie","75013", 49, 9],
            [75, "des Pyrénées - 20","399 bis rue des Pyrénées","75020", 79,6],
            [22831574, "Hôtel Parmentier","23 rue saint-ambroise","75011", 88,4],
            [184, "des Fontaines","2 rue des Fontaines du Temple","75003", 41, 8]]

class Hotel: #C++ style
    ID = 0
    name = 1
    address = 2
    code_postal = 3
    number_of_rooms = 4
    grade = 5

def input_to_loc(hotels):
    return [hotels[i][Hotel.address] + " " + hotels[i][Hotel.code_postal] for i in range(len(hotels))]

def parse_XML_geo(data):
    res = []
    root = PARSER.fromstring(data)
    i = 0 
    for result in root.getiterator("result"):
        for geometry in result.getiterator("geometry"):
            for location in geometry.getiterator("location"):
                for coordinates in list(location):
                    if coordinates.tag == "lat": 
                        lat = float(coordinates.text)
                    if coordinates.tag == "lng":
                        lng = float(coordinates.text)
                        res.append((lat,lng))
        i += 1
    return res 


def request_geolocation(loc):
    base_url = "https://maps.googleapis.com/maps/api/geocode/xml?"
    addresses = urllib.parse.quote_plus(loc[0])
    for i in range(1,len(loc)):
        addresses += "|"+urllib.parse.quote_plus(loc[i])
    url = base_url + "address=" + addresses + "&key="+ API_KEY_GEO
    xmltxt = requests.get(url).text
    return xmltxt


def get_geolocation(locations):
    n = len(locations)
    res = []
    for i in range(n):
        res += parse_XML_geo(request_geolocation(locations[i:i+1]))
    return res


def distance_vol(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin...

def matrice_vol(inputt):
    locations = input_to_loc(inputt)
    geolocations = get_geolocation(locations)
    n = len(geolocations)
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        lat1, lon1 = geolocations[i]
        for j in range(i):
            lat2, lon2 = geolocations[j]
            dist = distance_vol(lat1, lon1, lat2, lon2)
            matrix[i][j] = dist
            matrix[j][i] = dist
    return matrix

def parse_XML_route(data, loc):
    root = PARSER.fromstring(data)
    matrix = [[0 for _ in range(len(loc))] for _ in range(len(loc))]
    i=0
    for row in root.getiterator("row"):
        j=0
        for column in row.getiterator("element"):
            for duration in column.getiterator("duration"):
                for value in list(duration):
                    if value.tag == "value": 
                        matrix[i][j] = int(int(value.text)/60)+1
            j+=1
        i+=1
    return matrix

def request_route_voiture(ori, dest):
    base_url= "https://maps.googleapis.com/maps/api/distancematrix/xml?"  
    origins = urllib.parse.quote_plus(ori[0])
    for i in range(1, len(ori)): 
        origins += "|"+urllib.parse.quote_plus(ori[i])
    destinations = urllib.parse.quote_plus(dest[0])
    for i in range(1, len(dest)): 
        destinations += "|"+urllib.parse.quote_plus(dest[i])
    url = base_url+"origins="+origins+"&destinations="+destinations+"&key="+API_KEY
    xmltxt = requests.get(url).text
    return xmltxt

def request_route_transit(ori, dest):
    base_url= "https://maps.googleapis.com/maps/api/distancematrix/xml?"  
    origins = urllib.parse.quote_plus(ori[0])
    for i in range(1, len(ori)): 
        origins += "|"+urllib.parse.quote_plus(ori[i])
    destinations = urllib.parse.quote_plus(dest[0])
    for i in range(1, len(dest)): 
        destinations += "|"+urllib.parse.quote_plus(dest[i])
    url = base_url+"origins="+origins+"&destinations="+destinations+"&mode=transit&key="+API_KEY
    xmltxt = requests.get(url).text
    return xmltxt


def distance_transit(itin):
    res = {}
    travel = [(itin[i],itin[i+1]) for i in range(len(itin)-1)]
    for i in range(len(travel)) : 
        if (itin[i], itin[i+1]) in distance_dic[0].keys() : 
            travel.remove((itin[i], itin[i+1]))
            res[(itin[i], itin[i+1])] = distance_dic[0][(itin[i], itin[i+1])]
    if len(travel) == 0  : # we have already seen every travel
        return res 
    
    # otherwise, we need to call Google's API on those which are missing
    origins_list = input_to_loc([inputt[couple[0]] for couple in travel])
    destinations_list = input_to_loc([inputt[couple[1]] for couple in travel])
    matrix_transit = parse_XML_route(request_route_transit(origins_list,destinations_list), itin)
    # and add the data to the dictionary
    for i,couple in enumerate(travel):
        distance_dic[0][couple] = matrix_transit[i][i]
        res[couple] = matrix_transit[i][i]
    return res 

        
def distance_voiture(itin):
    res = {}
    travel = [(itin[i],itin[i+1]) for i in range(len(itin)-1)]
    for i in range(len(itin)-1) : 
        if (itin[i], itin[i+1]) in distance_dic[1].keys(): 
            travel.remove((itin[i], itin[i+1]))
            res[(itin[i], itin[i+1])] = distance_dic[1][(itin[i], itin[i+1])]
    if len(travel) == 0  : # we have already seen every travel
        return res 
    
    # otherwise, we need to call Google's API on those which are missing
    origins_list = input_to_loc([inputt[couple[0]] for couple in travel])
    destinations_list = input_to_loc([inputt[couple[1]] for couple in travel])
    matrix_transit = parse_XML_route(request_route_voiture(origins_list,destinations_list), itin)
    # and add the data to the dictionary
    for i,couple in enumerate(travel):
        distance_dic[1][couple] = matrix_transit[i][i]
        res[couple] = matrix_transit[i][i]
    return res 


def distances(itin, voiture_dispo): 
    # input : 
    # itin : itinerary = list of hotels 
    # voiture_dispo : boolean : 1 means yes, 0 means no
    res = [distance_transit(itin)]
    if voiture_dispo :
        res.append(distance_voiture(itin))
    a = [sum([res[0][i] for i in res[0]])] + ([sum([res[1][i] for i in res[1]])] if voiture_dispo else [])
    return a

print(distances([1,2,3],True))
