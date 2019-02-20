from info import *
import timematrices

###########################################
# LIRE L'INPUT A PARTIR DU FICHIER csv    #
###########################################
import pandas as pd
def read_input(filename):
    df = pd.read_csv(filename)
    df = df.loc[:, ['Id hôtel', 'nom', 'adresse', 'cp', 'nombre_chambres', 'decompte_score']]
    df.loc[:,['cp']] = df.loc[:,['cp']].astype(int).astype(str)
    inputt = df.values.tolist()
    return inputt


###########################################
# TRI DES HOTELS EN FONCTION DES SECTEURS #
###########################################

class H: 
    ID = 0
    name = 1
    address = 2
    CP = 3
    n_rooms = 4
    grade = 5

####################
# En considérant : 
# Secteur A : 75
# Secteur B : 93
# Secteur C : 92, 78, 95
# Secteur D : 77, 91, 94


def sort_input(inputt):
    sctA, sctB, sctC, sctD = [[] for _ in range(4)] 
    for hotel in inputt : 
        CP = str(hotel[H.CP])[:2]
        if CP == "75": sctA.append(hotel)
        if CP == "93": sctB.append(hotel)
        if CP in ["92","78","95"]: sctC.append(hotel)
        if CP in ["77", "91", "94"]: sctD.append(hotel)
    return (sctA, sctB, sctC, sctD)



#############################################
# TRI DES SALARIES EN FONCTION DES SECTEURS #
#############################################

####################
# En considérant : 
# Secteur A : 75
# Secteur B : 93
# Secteur C : 92, 78, 95
# Secteur D : 77, 91, 94



# Matrice donnant 
def ordering_M(M):
    M = [[(x, i) for i,x in enumerate(X)] for X in M]
    [X.sort(key = lambda x:x[0]) for X in M]
    M = [[x[1] for x in X] for X in M]
    return M 

