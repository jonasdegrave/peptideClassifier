# This routine plots proteins and peptides as horizontal bars highlighting regions of interest.
from config import *
import peptideClassifier
import os
import pandas as pd
from os.path import expanduser as ospath


def proteinSegments (M: int, N: int, peptides: list) -> list:
    if peptides == []:
        return [[PEPTIDE_OTHER, M, N]]

    peptide, a, b = peptides[0]

    ## Left-hand side
    # If the protein starts with the peptide
    if M == a:
        protein = [[peptide, M, b]]
    else:
        protein = [[PEPTIDE_OTHER, M, a-1], [peptide, a, b]]

    ## Right-hand side
    # If the protein ends with the peptide
    if N == b:
        return protein
    else:
        return protein + proteinSegments(b+1, N, peptides[1:])
 
# TESTS
# print(proteinSegments(1, 10, [["SIGNAL", 3, 5], ["PROPEP", 7, 8]]))
# print(proteinSegments(1, 473, [["SIGNAL", 51, 53], ["SIGNAL", 108, 120], ["PROPEP", 191, 234], ["PROPEP", 302, 415]]))

fileName = TEMP_FILES_FOLDER + "P08572.txt"

peptideSegments = peptideClassifier.getInterval(fileName)

# proteinSize = getProteinSize(fileName)
proteinSize = 1072

proteinSegments = proteinSegments(1, proteinSize, peptideSegments)

print()

proteinSegments = [['OTHER', 1, 50],
                    ['SIGNAL', 51, 53],
                    ['OTHER', 54, 107],
                    ['SIGNAL', 108, 120],
                    ['OTHER', 121, 190],
                    ['PROPEP', 191, 234],
                    ['OTHER', 235, 301],
                    ['PROPEP', 302, 415],
                    ['OTHER', 416, 473]]


def drawProtein (proteinSegments):
    pass


fileName = TEMP_FILES_FOLDER + "P08572.txt"

sheetFileName = INPUT_FILES_FOLDER + "A375.xlsx"

labels = ['PEPTIDE','PROPEP','SIGNAL']


def proteinData(sheetFileName):
    df=pd.read_excel(sheetFileName)
    field=["protein","Total Length","P1' position","Length Pep"]
    listProteinName=df[field[0]].values
    listProteinSize=df[field[1]].values
    listPepInitialRange=df[field[2]].values
    listPepFinalRange=df[field[3]].values
    return  listProteinName,  listProteinSize, listPepInitialRange, listPepFinalRange

for protein in zip(proteinData(sheetFileName)):
    proteinName, proteinSize, peptideInitialRange, peptideFinalRange = protein



# interval = peptideClassifier.getInterval (fileName)

# proteinSize = 1710

# print(interval)