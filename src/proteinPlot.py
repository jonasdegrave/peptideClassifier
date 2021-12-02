# This routine plots proteins and peptides as horizontal bars highlighting regions of interest.
from config import *
import peptideClassifier
import os

fileName = "./temp/" + "P08572.txt"

interval = peptideClassifier.getInterval (fileName)

proteinSize = 1710



print(interval)