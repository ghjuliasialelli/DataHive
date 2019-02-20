# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 19:30:57 2019

@author: Sebastien
"""

#import dist
from Trees import Tree
import info 
import timematrices
from dist import *
import math
import copy 
import sorting
import sorted_matrices

# LIMITES : 
# Il manque certaines implementations :
# - utilisation du paramtre NOMBRE_DE_PERSONNES
# - utilisation de la distance entre les salariés et le point de départ 
# - un parametre SECTEUR qu'on prend en compte, et qui donne VITESSE_MOYENNE_DANS_SECTEUR
# - disponibilité des salariés : ça doit etre un input, sous forme d'une liste des ids des salariés 

# L'implémentation a été pensée comme ceci : on lance plan_week(inputt,teams,M,blacklist_id) quand on
# veut connaitre le planning hebdomadaire de chaque équipe dans teams. 
# Parametres : 
#   (pas encore implémenté) secteur : secteur concerné  
#   inputt : spécifique à un secteur
#            liste d'objets H, cad d'hotels sous forme de listes, comportant les informations suivantes : 
#            [id, nom, adresse, code postal, nombre de chambres, score]
#   teams : liste des équipes, les équipes etant representees par des listes de id de salariés
#   M : matrice des temps de trajet (calculés à partir des distances à vol d'oiseau) entre tous les hotels de inputt
#   blacklist_id : 
# 
##############################################
# PARAMETRES UTILISÉS, modifiables à souhait #
##############################################

TEMPS_PAR_CHAMBRE = 5                           # temps en minutes passé dans chaque chambre
CHAMBRES_PAR_JOUR_PAR_PERSONNE = 30             # nombre de chambres visités / pers / jour
HEURES_PAR_JOUR = 7                             # heures de travail dans une journée
MAX_MINUTES = int((HEURES_PAR_JOUR) * 60)       
NOMBRE_DE_PERSONNE = 3                          # nombre de personnes dans une équipe
DAYS = 4                                        # nombre de jours dans la semaine où un employé travaille
VITESSE_MOYENNE_DANS_SECTEUR = 16               # vitesse moyenne de circulation dans le secteur (example : 16km/h dans Paris)
NOMBRE_CHAMBRES = 10                            # nombre arbitraire de chambres par hotel si non indiqué 

# in the 75 : 
DIST_MOYENNE = 51 
DISTANCE_PREMIER_QUARTILE = 8

# La ligne suivante permet de calculer la matrice des temps pour se rendre d'un hotel à un autre 
# basé sur leur distance à vol d'oiseau (et la vitesse moyenne de circulation dans le secteur)
# Appelle l'API Geolocation de Google, on peut donc essayer de minimiser les appels 
# Tant que de nouveaux hotels n'ont pas été ajoutés, pas besoin de la rappeler
# On peut donc dans un premier temps, print(M) apres avoir fait un appel, puis écrire la matrice 
# dans le fichier info.py, et commenter (#) la ligne suivante

M_75 = info.input_75                                # matrice des hotels 
M_dist_75 = timematrices.time_75                    # matrice des temps entre chaque hotels (calculé à partir des distances a vol d'oiseau)
indices_ord_75 = sorted_matrices.indices_ord_75     # pour l'hotel i, liste des hotels des moins au plus distants 


def list_sum(L):
    x = []
    for i in L:
        x += i
    return x

class H: 
    ID = 0
    name = 1
    address = 2
    CP = 3
    n_rooms = 4
    grade = 5

def temps_trajet(traj,M):
    return sum([M[traj[i]][traj[i+1]] for i in range(len(traj)-1)])

def score_function(iti,hotels,M):
    score = sum([hotels[h][H.n_rooms]*hotels[h][H.grade]/(i+1) for i,h in enumerate(iti[0])])
    score *= (iti[1] - 2*temps_trajet(iti[0],M))
    return score

def get_time_at_hotel(hotels,team_size):
    return [h[H.n_rooms]*TEMPS_PAR_CHAMBRE/team_size for h in hotels]

def compute_itinaries_from(M,time_at_hotel,i):
    n = len(time_at_hotel)
    tree = Tree(i,time_at_hotel[i])
    still_going = True
    t_leafs = tree.get_leafs()
    while still_going:
        leafs = copy.deepcopy(t_leafs)
        t_leafs = set()
        print("len of leafs ", len(leafs))
        for leaf in leafs:
            root = leaf.key
            for j in indices_ord_75[root]:
                if j not in leaf.parents:
                    if  M[leaf.key][j] > DISTANCE_PREMIER_QUARTILE : 
                        break
                    n_time = leaf.data + M[leaf.key][j] + time_at_hotel[j]
                    if n_time < MAX_MINUTES:
                        t_leafs.add(leaf.insert(j,n_time))
        if len(t_leafs) == 0:
            break
    return tree

# Associe un score à un certain itinéraire
def score_itis(hotels,itis,M):
    return [iti + [score_function(iti,hotels,M)] for iti in itis]

# Calcule tous les itinéraires possibles
def compute_all_itinaries(hotels,M,team_size):
    # hotels : tous les hotels que l'on veut visiter
    # M : matrice des temps entre les hotels
    # team_size : taille de l'équipe dont on veut planifier le planning
    n = len(hotels)
    time_at_hotel = get_time_at_hotel(hotels,team_size)
    itis = [compute_itinaries_from(M,time_at_hotel,i) for i in range(n)]
    #print(len(itis))
    itis = list_sum([tree.get_itis() for tree in itis])
    itis = score_itis(hotels,itis,M)
    itis.sort(key = lambda x : -x[2])
    return itis


# Aide pour planifier le planning hebdomataire des équipes
# Flexible et interactif : laisse le manager choisir quel itinéraire chaque équipe doit effectuer chaque jour
# En fonction du choix du manager pour le J0, propose des itinéraires adaptés pour J1, etc. 

def plan_week(inputt,teams,M,blacklist_id):
    # inputt : tout le data concernant les hotels (dont leurs scores)
    # teams : list avec les tailles des équipes (pour accéder à l'équipe en elle meme, appeler team_members[teams])
    # M : matrice avec les temps pour se rendre d'un hotel à un autre basé sur leur distance à vol d'oiseau (et la vitesse moyenne de circulation)
    # blacklist_id : set (vide initialement) contenant les id des hotels qu'on ne veut pas visiter cette semaine (aide pour la reprogrammation d'un planning
    # en pleine semaine lorsque la data base n'a pas encore été updatée)
    visited_h = set()
    for i,hotel in enumerate(inputt):
        if hotel[H.ID] in blacklist_id:
            visited_h.add(i)
    #print(visited_h)
    team_itis = [[] for _ in teams]
    itis_per_team_size = {}
    for team in range(len(teams)):
        itis_per_team_size[team] = compute_all_itinaries(inputt,M,teams[team])
        itis_per_team_size[team].sort(key = lambda x : -x[2])
    for _ in range(DAYS):
        for i in range(len(teams)):
            for t in itis_per_team_size:
                t_rm = []
                for j,iti in enumerate(itis_per_team_size[t]):
                    for h in visited_h:
                        if h in iti[0]:
                            t_rm.append(j)
                            break
                for j in reversed(t_rm):
                    itis_per_team_size[t].pop(j)
            if len(itis_per_team_size[i]) == 0:
                continue
            print("-----------------")
            print("Pour l'équipe {} avec {} personnes :".format(i,teams[i]))
            for iti in itis_per_team_size[i][:3]:
                for h in iti[0]:
                    print(inputt[h][H.name])
                print('Cet itinéraire prendra environ {} heures'.format(round(iti[1]/60,2)))
                x = distances(iti[0],voiture[i])
                print('Dont {} minutes en transport'.format(x[0]) + (' ou dont {} minutes en voiture'.format(x[1]) if voiture[i] else ''))
                print()
            x = int(input('Choisir un itinéraire: '))-1
            team_itis[i].append(itis_per_team_size[i][x])
            visited_h.update(set(itis_per_team_size[i][x][0]))
    i=0
    for team in team_itis:
        print("---------------------------------")
        print("Planning pour l'équipe {}".format(i))
        print()
        for iti in team:
            for h in iti[0]:
                print(inputt[h][H.name])
            print('Prendra environ {} heures'.format(round(iti[1]/60,2)))
            print() 
        i+=1
    print("Résumé des itinéraires de la semaine : ", team_itis)


"""

class Var:
    M = 0                       # matrice des hotels 
    M_dist = 1                  # matrice des distances entre chaque hotels 
    indices_ord = 2             # matrice des distances ordonée 
    v = 3                       # vitesse moyenne dans le secteur (16 pour le 75)
    d = 4                       # distance moyenne entre deux hotels dans le secteur (51 pour le 75)


####################
# En considérant : 
# Secteur A/0 : 75
# Secteur B/1 : 93
# Secteur C/2 : 92, 78, 95
# Secteur D/3 : 77, 91, 94


def plan_week(sect):
    if sect == 75 : 
        i = 0
    if sect == 93 : 
        i = 1
    if sect in [92,78,95]:
        i = 2
    if sect in [77,91,94]:
        i = 3
    
    M = Sect[i][Var.M] 
    M_dist = Sect[i][Var.M_dist]
    indices_ord = Sect[i][Var.indices_ord]
    VITESSE_MOYENNE_DANS_SECTEUR = Sect[i][Var.v]
    DIST_MOYENNE = Sect[i][Var.d]

    plan_week(M,info.teams,M,set()) 

plan_week(75)

"""

plan_week(M_75,info.teams,M_dist_75,set()) 


