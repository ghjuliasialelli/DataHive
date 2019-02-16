# inputt with hotels in different sectors, we want one matrix per sector
inputt =    [[225,"Grand Hôtel d'Aboukir", "134 rue d'Aboukir","75002", 35, 7], 
            [7180332, "Chaussée d'Antin", "46 rue de la Chaussée d'Antin", "93009", 34, 3],
            [3029096, "Métropolitain", "158 rue Oberkampf", "92011", 60, 5],
            [69, "Cristal","64 rue de la Jonquière","78017", 98, 10],
            [160, "des Beaux-Arts","4 rue André Antoine","95018", 76, 2],
            [14664544, "Moderne - Paris 20ème","57 rue de la Réunion","77020", 41,10],
            [7923060, "Sofiane","66 boulevard de Charonne","91020",47,2],
            [7877630, "Hipotel Paris Buttes Chaumont","7 rue Jean Baptiste Dumay","94020", 73,5],
            [130, "de Normandie", "4 rue d'Amsterdam","75009", 200,3],
            [5928342, "Maison Blanche","107 Bis Avenue d'Italie","75013", 49, 9],
            [75, "des Pyrénées - 20","399 bis rue des Pyrénées","93020", 79,6],
            [22831574, "Hôtel Parmentier","23 rue saint-ambroise","92011", 88,4],
            [184, "des Fontaines","2 rue des Fontaines du Temple","77003", 41, 8]]


class H: #C++ style
    ID = 0
    name = 1
    address = 2
    CP = 3
    number_of_rooms = 4
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
        CP = hotel[H.CP][:2]
        if CP == "75": sctA.append(hotel)
        if CP == "93": sctB.append(hotel)
        if CP in ["92","78","95"]: sctC.append(hotel)
        if CP in ["77", "91", "94"]: sctD.append(hotel)
    return (sctA, sctB, sctC, sctD)





