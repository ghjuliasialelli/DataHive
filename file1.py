# XML PARSING 
import xml.etree.ElementTree as PARSER
# Percent encoding
import urllib.parse
# For HTTP requests
import requests
    
def matrix_driving(base_url, origins, locations):
    url = base_url+"origins="+origins+"&destinations="+origins+"&key="+API_KEY
    r_driving = requests.get(url)
    data_driving = r_driving.text

    # Parse input XML for driving 
    root_driving = PARSER.fromstring(data_driving)
    driving_matrix = [[0 for _ in range(len(locations))] for _ in range(len(locations))]

    i=0
    for row in root_driving.getiterator("row"):
        j = 0
        for column in row.getiterator("element"):
            for duration in column.getiterator("duration"):
                for value in list(duration):
                    if value.tag == "value": 
                        driving_matrix[i][j] = int(int(value.text)/60)+1
            j+=1
        i+=1
    return driving_matrix

def matrix_transit(base_url, origins, locations):
    url = base_url+"origins="+origins+"&destinations="+origins+"&mode=transit&key="+API_KEY
    r_transit = requests.get(url)
    data_transit = r_transit.text

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
                        transit_matrix[i][j] = int(int(value.text)/60)+1
            j+=1
        i+=1

    return transit_matrix

def distance_matrix(voiture_dispo, locations):
    base_url= "https://maps.googleapis.com/maps/api/distancematrix/xml?"  

    origins = urllib.parse.quote_plus(locations[0])
    for i in range(1, len(locations)):
        origins = origins+"|"+urllib.parse.quote_plus(locations[i])

    matrix_t = matrix_transit(base_url, origins, locations)
    res = [matrix_t]
    if voiture_dispo : 
        matrix_d = matrix_driving(base_url, origins, locations)
        res.append(matrix_d)
    return res 
    
