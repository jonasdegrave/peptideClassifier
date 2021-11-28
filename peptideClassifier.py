import os
import pandas as pd
import requests
from time import time
from multiprocessing.pool import ThreadPool
from clint.textui import progress

url = 'http://do1.dr-chuck.com/pythonlearn/EN_us/pythonlearn.pdf'

r = requests.get(url, stream=True)

with open("LearnPython.pdf", "wb") as Pypdf:

    total_length = int(r.headers.get('content-length'))

    for ch in progress.bar(r.iter_content(chunk_size = 2391975), expected_size=(total_length/1024) + 1):

        if ch:

            Pypdf.write(ch)





# If enabled, prints debug messages to console;
DEBUG = False

#  Recebe o nome de arquivo e retorna uma lista de linhas com intervalos de classes
def filterFile(fileName):
    # if not fileExists("./temp/{}".format(fileName)):
    #     print("File {} doesn't exist, downloading...".format(fileName))
    #     os.system("curl https://www.uniprot.org/uniprot/{} > ./temp/{}".format(
    #       fileName,
    #      fileName))

    arq = open("./temp/{}".format(fileName), "r")
    contents = arq.read()
    arq.close()

    lines = contents.split('\n')

    keys = ["SIGNAL", "PROPEP"]

    results = []

    for key in keys:
        results += list(filter(lambda line: key in line, lines))

    results = list(map(lambda line: line.split(), results))

    final = []

    for result in results:
        interval = result[2].split("..")
        final += [[result[1], int(interval[0]), int(interval[1])]]

    return final

# Recebe uma lista de intervalos e um numero, e determina a classe
def classifier (number, intervals):
    for interval in intervals:
        if number >= interval[1] and number <= interval[2]:
            return interval[0]
    return "OTHER"

def getSheet (fileName):
    return pd.read_excel(fileName)

def main (sheetName):
    sheetContents = getSheet(sheetName)
    
    # We skip first line because the sheet has a header;
    for line in sheetContents[1:]:
        # 5th column corresponds to 'protein code';
        protein = line[4]

        # 11th column corresponds to 'P1 position';
        position = line[10]
    
        protein


    #contents=df.iloc[:,3]
    #=df.iloc[:,4]



if __name__ == "__main__":
    if len(os.sys.argv) != 2:
        print("[Error] Expecting 1 argument. Usage:\n\t$ python peptideClassifier.py <sheetName.xlsx>")
        os.sys.exit(1)
    sheetName = os.sys.argv[1]
    main(sheetName)

    



    # planilha = open(nomePlanilha, "r")
    # conteudo = planilha.readlines()
    # planilha.close()
    

    #u = UniProt()
    #r=Rhea()

    #getPeptide()
    #testing_HTML()

    # interval = filterFile("P09681.txt")

    # print(intervalo)

    # elementos = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    # for elemento in elementos:
    #     print("Elemento: {} classificado como {}".format(elemento, classificador(elemento, intervalo)))

