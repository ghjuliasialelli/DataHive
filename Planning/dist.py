# XML PARSING 
import xml.etree.ElementTree as PARSER
# Percent encoding
import urllib.parse
# For HTTP requests
import requests
# For Haversinee formula
from math import cos, asin, sqrt

import info 

API_KEY = "AIzaSyDSlnWcTV2bIenN_JTnn6BzLNeBI0tHOtA"
API_KEY_GEO = "AIzaSyBcjo9aomsuIHltAcczyrOJJXZIkrGy0vk"

# Liste de dictionaires avec les distances entre les hotels 
distance_dic = [{},{}]
# distance_dic[0] : distances en transports en commun
# distance_dic[1] : distances en voiture
# On procede ainsi parce qu'on est toujours sur de devoir compute les distances en transports

"""
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
"""

class H: 
    ID = 0
    name = 1
    address = 2
    CP = 3
    n_rooms = 4
    grade = 5

def input_to_loc(hotels):
    return [hotels[i][H.address] + " " + hotels[i][H.CP] for i in range(len(hotels))]


################################################
# Utilisation de l'API Geolocation de Google   #
# Calcul des coordonnées des adresses          #
# Et des distances à vol d'oiseau              #
################################################

# Rend une liste des coordonnées (lat, lng) à partir d'un XML 
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

# Lance une requete à l'API de Google pour obtenir les coordonnées 
def request_geolocation(loc):
    base_url = "https://maps.googleapis.com/maps/api/geocode/xml?"
    addresses = urllib.parse.quote_plus(loc[0])
    for i in range(1,len(loc)):
        addresses += "|"+urllib.parse.quote_plus(loc[i])
    url = base_url + "address=" + addresses + "&key="+ API_KEY_GEO
    xmltxt = requests.get(url).text
    return xmltxt

# Wrapper function : 
def get_geolocation(locations):
    print('get geolocation function :', len(locations))
    n = len(locations)
    res = []
    print("FUCKING n ",n)
    for i in range(n):
        print('     in geo :', (i/n)*100)
        print("    len res avant insertion :", len(res))
        print("     locations[] :", locations[i:i+1])
        t = parse_XML_geo(request_geolocation(locations[i:i+1]))
        print(len(t))
        res.append(t[0])
        print("    len res apres insertion :", len(res))
    print("         len of the output :", len(res))
    return res

# Calcule la distance à vol d'oiseau entre deux points 
def distance_vol(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin...

# Calcule la matrice des distances à vol d'oiseau entre les adresses données dans inputt
def matrice_vol(inputt):
    print("matrice_vol function")
    print("     len of input :", len(inputt))
    locations = input_to_loc(inputt)
    print("      len of locations (conversion)", len(locations))
    geolocations = get_geolocation(locations)
    print("       len of geolocations :", len(geolocations))
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



################################################
# Utilisation de l'API Route de Google         #
# Calcul des temps en voiture ou en tranport   #
################################################

# Lit le XML et rend la matrice des distances 
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

# Lance une requete à Google pour obtenir les temps en voiture entre les points dans ori et les points dans dest
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

# Lance une requete à Google pour obtenir les temps en transports entre les points dans ori et les points dans dest
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

# Temps en transports en commun entre les points de l'itinéraire
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

# Temps en voiture entre les points de l'itinéraire 
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

# Wrapper function : rend la durée totale d'un itinéraire 
# En transports et/ou en voiture, en fonction de la valeur du booléen voiture_dispo
def distances(itin, voiture_dispo): 
    # input : 
    # itin : itinerary = list of hotels 
    # voiture_dispo : boolean : 1 means yes, 0 means no
    res = [distance_transit(itin)]
    if voiture_dispo :
        res.append(distance_voiture(itin))
    a = [sum([res[0][i] for i in res[0]])] + ([sum([res[1][i] for i in res[1]])] if voiture_dispo else [])
    return a



############################################
# Calcul distance maison employé / hotel   #
############################################

# Output : liste des distances entre chaque employé et les points de départ
# Format : [[*liste de distances entre chaque employé et point1*], 
#           [*liste de distances entre chaque employé et point2*],
#               ...                                               ]  
def distance_from_team(team_index, points):
    # team_index : index de l'équipe dont on veut calculer les distances
    # points : liste de points de départ potentiels pour l'itinéraire
    team = teams[team_index]
    addresses = [construct_address(employe) for employe in team]
    geo = get_geolocation(addresses)   # localisation de chaque membre de l'équipe
    distances = []
    for person in geo:
        dist = []
        for point in point: 
            lat1, lon1 = person[0], person[1]
            lat2, lon2 = point[0], point[1]
            dist.append(distdistance_vol(lat1, lon1, lat2, lon2))
        distances.append(dist)
    return distances

# Classe de salariés, facilite l'accès à la base de données
# Ne considère pas les disponibilités. 
# Le manager devra rentrer manuellement qui fait partie de quelle équipe 
# pour les 4 jours de la semaine. 
class S: 
    nom = 0
    prénom = 1
    num_voie = 2
    non_identifie = 3   # pas compris ce que la colonne D du fichier excel représente
    nom_voie = 4
    localite = 5
    CP = 6
    permis = 7
    secteur = 8         # liste des secteurs couverts

def construct_address(person):
    # Idéalement, 'person' serait un id_employe. Facilite l'accès à la base de donnée
    # Implémentation effectuée avec cette assumption
    # Prend l'id d'un employé et rend une adresse utilisable par l'API de Google maps sous forme de string
    # Format de l'adresse : Num voie + Nom voie + Localité + Code postal
    return data_salarie[person].num_voie + " " +  data_salarie[person].nom_voie + " " +  data_salarie[person].localite + " " +  data_salarie[person].CP

