# This routine plots proteins and peptides as horizontal bars highlighting regions of interest.
from config import *
import peptideClassifier
import os
import pandas as pd
from os.path import expanduser as ospath
import itertools

fileName = TEMP_FILES_FOLDER + "P08572.txt"

sheetFileName = INPUT_FILES_FOLDER + "A375.xlsx"

labels = ['PEPTIDE','PROPEP','SIGNAL']
def proteinData(sheetFileName):
    df=pd.read_excel(sheetFileName)
    field=["protein","Total Length","P1' position","Length Pep"]
    listProteinName=df[field[0]].to_list()
    listProteinSize=df[field[1]].to_list()
    listPepInitialRange=df[field[2]].to_list()
    listPepFinalRange=df[field[3]].to_list()
    listData=[]
    for protein in zip(listProteinName,listProteinSize,listPepInitialRange,listPepFinalRange):
        listData.append(protein)
    return listData

#print(proteinData(sheetFileName))
#array_data= zip(proteinData(sheetFileName))
#print(list(array_data))


#def proteinSegments(M,N,peptides):
def proteinSegments (M: int, N: int, peptides: list) -> list:
    if peptides == []:
        return [[PEPTIDE_OTHER, M, N]]

    peptide = peptides[0]
    peptideType, a, b = peptide[0], peptide[1], peptide[2]

    ## Left-hand side
    # If the protein starts with the peptide
    if M == a:
        protein = [[peptideType, M, b]]
    else:
        protein = [[PEPTIDE_OTHER, M, a-1], [peptideType, a, b]]

    ## Right-hand side
    # If the protein ends with the peptide
    if N == b:
        return protein
    else:
        return protein + proteinSegments(b+1, N, peptides[1:])
 
# TESTS
# print(proteinSegments(1, 10, [["SIGNAL", 3, 5], ["PROPEP", 7, 8]]))
# print(proteinSegments(1, 473, [["SIGNAL", 51, 53], ["SIGNAL", 108, 120], ["PROPEP", 191, 234], ["PROPEP", 302, 415]]))
for protein in proteinData(sheetFileName):
    proteinName, proteinSize, pepInitialLen, pepFinalLen = protein

    peptides=[["PEP", pepInitialLen, pepFinalLen]]

    print("\n\n")
    print("\nPeptides: {}\n".format(peptides))
    print("\nProtein Size: {}\n".format(proteinSize))
    segments = proteinSegments(1, proteinSize, peptides)
    print("\nSegments: {}\n".format(segments))
    print("\n\n")

fileName = TEMP_FILES_FOLDER + "P08572.txt"

#peptideSegments = peptideClassifier.getInterval(fileName)

# proteinSize = getProteinSize(fileName)
proteinSize = 1072

#proteinSegments = proteinSegments(1, proteinSize, peptideSegments)


def drawProtein (proteinSegments):
    pass



# interval = peptideClassifier.getInterval (fileName)

# proteinSize = 1710

# print(interval)