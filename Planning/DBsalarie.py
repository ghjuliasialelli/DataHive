import xlrd
loc = "salarie.xlsx"
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

rows = [1, 5, 8,10,13,16,20,22,25,28,32,35,38,42,46]
columns = [0,1,2,3,4,5,6,7,10,11,12,13]
numbers = [2,6]
secteurs = [10,11,12,13]
data_salarie = {}
# Pour l'instant, on considere que les id des employés sont leur ligne d'apparition dans le fichier Excel
# À terme, il faut les remplacer par des vrais ID pour que le manager ait acces facilement  

for i in rows:
    informations = []
    sct = []
    for j in columns:
        if j in numbers: 
            informations.append(  str(int(sheet.cell_value(i,j)) )  )
        elif j in secteurs :
            if sheet.cell_value(i,j) != '':
                sct.append( str(int(sheet.cell_value(i,j)) ) )
        elif j == 7 :
            if sheet.cell_value(i,j)=="NON": 
                val = 0
            if sheet.cell_value(i,j)=="OUI": 
                val = 1
            informations.append(val)
        else :
            informations.append(sheet.cell_value(i,j))
    informations.append(sct)
    data_salarie[str(i+1)] = informations

print(data_salarie)