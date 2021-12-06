# This routine plots proteins and peptides as horizontal bars highlighting regions of interest.
from config import *
import peptideClassifier
import os
import pandas as pd
from os.path import expanduser as ospath



fileName = "./temp/" + "P08572.txt"

sheetName= "/home/naiane/Documents/Doutorado/Software/peptideClassifier/inputFiles/" + "A375.xlsx"

labels = ['PEPTIDE','PROPEP','SIGNAL']
colors = ['#1D2F6F', '#8390FA', '#6EAF46']

df=pd.read_excel(ospath(sheetName))


def data(sheet):
    field=["protein","Total Length","P1' position","Length Pep"]
    listProteinName=df[field[0]].values
    listProteinSize=df[field[1]].values
    listPepInitialRange=df[field[2]].values
    listPepFinalRange=df[field[3]].values
    return  listProteinName,  listProteinSize, listPepInitialRange, listPepFinalRange

data(df)


interval = peptideClassifier.getInterval (fileName)

proteinSize = 1710



print(interval)