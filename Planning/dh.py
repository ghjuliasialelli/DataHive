# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 19:30:57 2019

@author: Sebastien
"""

#import dist
from Trees import Tree
from info import *


TEMPS_PAR_CHAMBRE = 5
CHAMBRES_PAR_JOUR_PAR_PERSONNE = 30
HEURES_PAR_JOUR = 7
MAX_MINUTES = int((HEURES_PAR_JOUR) * 60)
NOMBRE_DE_PERSONNE = 3
DAYS = 4
VITESSE_MOYENNE_DANS_SECTEUR = 16

#M = [[i/VITESSE_MOYENNE_DANS_SECTEUR*60 for i in X] for X in dist.matrice_vol(inputt)]

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
    while still_going:
        still_going = False
        for leaf in tree.get_leafs():
            for j in range(n):
                if j not in leaf.parents:
                    n_time = leaf.data + M[leaf.key][j] + time_at_hotel[j]
                    if n_time < MAX_MINUTES:
                        leaf.insert(j,n_time)
                        still_going = True
    return tree

def score_itis(hotels,itis,M):
    return [iti + [score_function(iti,hotels,M)] for iti in itis]


def compute_all_itinaries(hotels,M,team_size):
    n = len(hotels)
    time_at_hotel = get_time_at_hotel(hotels,team_size)
    itis = [compute_itinaries_from(M,time_at_hotel,i) for i in range(n)]
    itis = list_sum([tree.get_itis() for tree in itis])
    itis = score_itis(hotels,itis,M)
    itis.sort(key = lambda x : -x[2])
    return itis

def plan_week(inputt,teams,M):
    team_itis = [[] for _ in teams]
    itis_per_team_size = {}
    for team in range(len(teams)):
        itis_per_team_size[team] = compute_all_itinaries(inputt,M,teams[team])
        itis_per_team_size[team].sort(key = lambda x : -x[2])
    visited_h = set()
    for _ in range(DAYS):
        for i in range(len(teams)):
            if len(itis_per_team_size[i]) == 0:
                continue
            print('For team {} with {} people :'.format(i,teams[i]))
            for iti in itis_per_team_size[i][:3]:
                for h in iti[0]:
                    print(inputt[h][H.name])
                print('It will take {} hours'.format(iti[1]/60))
                print()
            x = int(input('Choose one: '))-1
            team_itis[i].append(itis_per_team_size[i][x])
            visited_h.update(set(itis_per_team_size[i][x][0]))
            for t in itis_per_team_size:
                t_rm = []
                for i,iti in enumerate(itis_per_team_size[t]):
                    for h in visited_h:
                        if h in iti[0]:
                            t_rm.append(i)
                            break
                for i in reversed(t_rm):
                    itis_per_team_size[t].pop(i)
    for team in team_itis:
        print('Planning for team')
        print()
        for iti in team:
            for h in iti[0]:
                print(inputt[h][H.name])
            print('It will take {} hours'.format(iti[1]/60))
            print() 

plan_week(inputt,teams,M)

                   
            
        
    
    
    