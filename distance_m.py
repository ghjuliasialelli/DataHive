# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 10:29:14 2019

@author: Sebastien
"""

# XML PARSING 
import xml.etree.ElementTree as PARSER
# Percent encoding
import urllib.parse
# For HTTP requests
import requests

API_KEY = "AIzaSyDSlnWcTV2bIenN_JTnn6BzLNeBI0tHOtA"

class Hotel: #C++ style
    ID = 0
    name = 1
    address = 2
    code_postal = 3
    number_of_rooms = 4
    grade = 5
    
def matrix_driving(base_url,origins,locations):
    params_driving = {'origins':origins, 'destinations':origins, 'key':API_KEY}
    r_driving = requests.get(base_url, params=params_driving)
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
                        print("i,j", (i,j))
                        driving_matrix[i][j] = int(value.text)/60
            j+=1
        i+=1
    return driving_matrix

def matrix_transit(base_url,origins,locations):
    params_transit = {'origins':origins, 'destinations':origins, 'mode':'transit', 'key':API_KEY}
    r_transit = requests.get(base_url, params=params_transit)
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
                        transit_matrix[i][j] = int(value.text)/60
            j+=1
        i+=1
    return transit_matrix




def distance_matrix(voiture_dispo,locations):
    base_url= "https://maps.googleapis.com/maps/api/distancematrix/xml" # pas de '?' a la fin en utilisant requests 
    
    origins = urllib.parse.quote_plus(locations[0])
    for i in range(1, len(locations)):
        origins = origins+"|"+urllib.parse.quote_plus(locations[i])
    m_transit = matrix_transit(base_url,origins,locations)
    res = [m_transit]
    if voiture_dispo: 
        m_driving = matrix_driving(base_url,origins,locations)
        res.append(m_driving)
    return res 

def distance_matrix_g(voiture_dispo,hotels):
    locations = [hotels[i][Hotel.address] + " " + hotels[i][Hotel.code_postal] for i in range(len(hotels))]
    return distance_matrix(voiture_dispo,locations)
