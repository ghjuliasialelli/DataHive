# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 19:30:57 2019

@author: Sebastien
"""

TEMPS_PAR_CHAMBRE = 10
CHAMBRES_PAR_JOUR_PAR_PERSONNE = 30
HEURES_PAR_JOUR = 7.5
MAX_MINUTES = int(HEURES_PAR_JOUR * 60)
NOMBRE_DE_PERSONNE = 3

data = [['id1','hotel1','somewhere',30,5],['id1','hotel1','somewhere',3,2],
        ['id1','hotel1','somewhere',10,10],['id1','hotel1','somewhere',100,7],
        ['id1','hotel1','somewhere',15,1],['id1','hotel1','somewhere',70,10]]
M = [[59, 30, 20, 25, 26, 50],
     [34, 43, 53, 58, 37, 38],
     [34, 57, 57, 22, 34, 17],
     [29, 47, 22, 17, 40, 53],
     [12, 47, 56, 25, 18, 25],
     [48, 52, 45, 39, 36, 30]]

def score_function(hotel):
    return hotel[Hotel.number_of_rooms]*hotel[Hotel.grade]

class Hotel: #C++ style
    ID = 0
    name = 1
    address = 2
    number_of_rooms = 3
    grade = 4
    
class Tree:
    def __init__(self,key,data):
        self.root = Node(key,data,set([key]))
        
    def get_leafs(self):
        return self.root.get_leafs()

    def get_itis(self):
        return self.root.get_itis([])
class Node:
    def __init__(self,key,data,parents):
        self.key = key
        self.data = data
        self.children = {}
        self.parents = parents
        
    def insert(self,key,data):
        parents = self.parents.union([key])
        self.children[key] = Node(key,data,parents)
        
    def get_leafs(self):
        if len(self.children) == 0:
            return [self]
        sol = []
        for key in self.children:
            sol += self.children[key].get_leafs()
        return sol

    def get_itis(self,path):
        path  = path + [self.key]
        if len(self.children) == 0:
            return [(path,self.data)]
        itis = []
        for key in self.children:
            itis += self.children[key].get_itis(path)
        return itis

def get_time_at_hotel(hotels):
    time_at_hotel = []
    for i in range(len(hotels)):
        time_at_hotel.append(int(hotels[i][Hotel.number_of_rooms]*TEMPS_PAR_CHAMBRE/NOMBRE_DE_PERSONNE))
    return time_at_hotel

def compute_all_itinaries(hotels,M): #traject time matrix
    n = len(hotels)
    time_at_hotel = get_time_at_hotel(hotels)
    itis = []
    for i in range(n):
        itis.append(compute_itinaries_from(M,time_at_hotel,i))
    a_itis = []
    for tree in itis:
        a_itis += tree.get_itis()
    a_itis = score_itis(hotels,a_itis)
    a_itis.sort(key = lambda x : x[2])
    print(a_itis)
            
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

def score_itis(hotels,itis):
    must = {i for i in range(len(hotels)) if hotels[i][Hotel.grade] == 10}
    scored_itis = []
    for iti in itis:
        score = 0
        for i in range(len(iti[0])):
            score += score_function(hotels[iti[0][i]])/(i+1)**2
        if len(must.difference(set(iti[0]))) == 0:
            scored_itis.append(list(iti) + [score/iti[1]])
    return scored_itis
    

compute_all_itinaries(data,M)
                   
            
        
    
    
    