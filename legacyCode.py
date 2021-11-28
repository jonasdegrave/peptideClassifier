import xlsxwriter
import os
import re
import pandas as pd
from bs4 import BeautifulSoup
import urllib3
import matplotlib.pyplot as plt

#import requests
#import glob
#import numpy as np

#import xml.etree.ElementTree as ET
#import urllib.request
#from collections import Counter
#from bioservices import UniProt
#import urllib.parse
#import urllib.request
#from bioservices import Rhea



def getPeptide():
    workbook=xlsxwriter.Workbook('sequences_remade.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0,0,"Sequences")
    worksheet.write(0,1,"Seq_ID (Uniprot)")
    worksheet.write(0,2,"Total Length")
    worksheet.write(0,3,"P1' position")
    worksheet.write(0,4,"5 Before")
    worksheet.write(0,5,"5 After")
    worksheet.write(0,6,"P1")
    worksheet.write(0,7,"Acetilation")
    worksheet.write(0,8,"Remarks-1")
    worksheet.write(0,9,"Remarks-2")
    worksheet.write(0,10,"Remarks-3")
    worksheet.write(0,11,"P1'")
    worksheet.write(0,12,"Sequence Raw")
    worksheet.write(0,13,"Remarks-4")
    row=1
    df=pd.read_excel('para_testar_A375.xlsx')
    contents=df.iloc[:,3]
    files=df.iloc[:,4]
    #print(files)
    count=0
    count_2=0
    column=0
    row_8=1
    row_10=1
    row_12=1
    row_13=1
    col_13=13
    count_met=0
    count_nonmet=0
    m=["M"]
    for line_2 in contents:
        #print (content)
        x=re.sub("[\(\[].*?[\)\]]", "", line_2)
        #print(x)
        search=x[3:-3]
        #print(search)
        writing_sequence=worksheet.write(row,column,search)
        column+=1
        writing_sequence=worksheet.write(row,column,files[count])
        column+=1
        files_fasta="./fasta/"+files[count]+".fasta"
        count+=1
        print(files[count])
        try:
            with open (files_fasta) as f:
                next(f)
                seq=""
                c=0
                #url='https://www.uniprot.org/uniprot/Q99832'
                url="https://www.uniprot.org/uniprot/%s"%(files[count])
                http=urllib3.PoolManager()
                r=http.request('GET',url)
                content=r.data
                content=content.decode("utf-8")
                soup = BeautifulSoup(content, 'html.parser') 
                pep=content.find("Signal peptide")
                nat=content.find("Natural variant")
                poly=content.find("Propeptide")
                for line in f:
                    c=c+len(line)-1
                    seq+=line
                   # print(seq)
                seq = seq.replace("\n", "")
                find=seq.find(search)+1
                writing_protein=worksheet.write(row,column,c)
                column+=1
                writing_sequence=worksheet.write(row,column,find)
                column+=1
                col_8=8
                col_10=10
                list_natural=[1,2,3]
                #print(line[0])
                col_12=12
                writing_sequence=worksheet.write(row_12,col_12,line_2)
                row_12+=1
                bf_pep1=seq[:find-1]
                bf_pep=bf_pep1[-5:]
                af_pep1=seq[find:]
                af_pep1=af_pep1.strip(search)
                af_pep=af_pep1[:5]
                writing_sequence=worksheet.write(row,column,bf_pep)   
                column+=1
                writing_sequence=worksheet.write(row,column,af_pep)
                #print(bf_pep1)
                if find in list_natural:
                    writing_col_8=worksheet.write(row_8,col_8,"Natural")
                    row_8+=1
                    if "M" in bf_pep:
                       writing_met=worksheet.write(row_10,col_10,"Met-removed")
                       row_10+=1
                       count_met+=1
                       #print(line_2[0])
                    else:
                        if line_2[0] != "M":
                            writing_met=worksheet.write(row_10,col_10,"Met-intact")
                            row_10+=1
                            count_nonmet+=1    
                            #print(r_10)
                else:
                    writing_col_8=worksheet.write(row_8,col_8,"Neo N-terminus")
                    row_8+=1
                    row_10+=1

                #get webpage content from unitprot to find natural, signal peptide and polypeptide

                if pep > 0:
                    y = soup.find('a', {'title' : 'BLAST subsequence'})
                    y=str(y)
                    number=y[-6:-4]  
                    number=int(number)
                    if find < number:
                        writing_col_13=worksheet.write(row_13,col_13,"Signal Peptide")
                        row_13+=1
                        print(number)
                        number=""  
                #elif nat > 0:
                #    writing_col_13=worksheet.write(row_13,col_13,"Natural variant")
                #    row_13+=1
                elif poly>0:
                    y = soup.find('a', {'title' : 'BLAST subsequence'})
                    y=str(y)
                    number=y[-6:-4]  
                    number=int(number)
                    if find < number:
                        writing_col_13=worksheet.write(row_13,col_13,"Signal Peptide")
                        row_13+=1
                        print(number)
                        number=""
                    writing_col_13=worksheet.write(row_13,col_13,"Propeptide")
                    row_13+=1
                elif pep < 0 and nat <0 and poly <0:
                    #writing_col_13=worksheet.write(row_13,col_13,"Polypeptide")
                    row_13+=1
                print(pep,nat,poly)
                    #print(af_pep)

        except StopIteration:
            pass     
        row+=1
        column=0 
    try:
        r=1
        r_2=1
        r_11=1
        count_acetilated=0
        count_nonacetilated=0
        for raw_data in contents:
            #print(raw_data[0])
            acetilation_code="43.02"
            acetilation_finder=raw_data.find(acetilation_code)
            #print(acetilation_finder)
            col_2=6
            col_11=11
            writing_sequence=worksheet.write(r_2,col_2,raw_data[0])
            r_2+=1
            writing_sequence=worksheet.write(r_11,col_11,raw_data[10])
            r_11+=1
            col=7
            if acetilation_finder > 0:
                writing_sequence=worksheet.write(r,col,"Acetilated")
                r+=1
                count_acetilated+=1
            else:
                writing_sequence=worksheet.write(r,col,"Free")
                r+=1
                count_nonacetilated+=1

        total=count_nonacetilated+count_acetilated
        acetilated_per=(count_acetilated/total)*100
        nonacetilated_per=(count_nonacetilated/total)*100
        my_data=[acetilated_per,nonacetilated_per]
        my_labels='Acetilated', 'Free'
        my_colors = ['lightblue','lightsteelblue','silver']
        plt.pie(my_data,labels=my_labels,autopct='%1.1f%%', colors=my_colors,textprops={'fontsize': 14})
        fig = plt.gcf()
        #fig.set_size_inches(10,10)
        #plt.show()
        imagefile="acetilation.png"
        fig.savefig(imagefile,dpi=150)
        plt.close(fig)

        total=count_nonmet+count_met
        met_per=(count_met/total)*100
        nonmet_per=(count_nonmet/total)*100
        my_data=[met_per,nonmet_per]
        my_labels='Met-Removed', 'Met-Intact'
        my_colors = ['lightblue','lightsteelblue','silver']
        plt.pie(my_data,labels=my_labels,autopct='%1.1f%%', colors=my_colors,textprops={'fontsize': 14})
        fig = plt.gcf()
        fig.set_size_inches(10,10)
        plt.show()
        imagefile="met.png"
        fig.savefig(imagefile,dpi=150)
        plt.close(fig)
    except StopIteration:
        pass   
  
    workbook.close()
    return()



def testing_HTML(content):
    try:
        workbook=xlsxwriter.Workbook('sequences_remade.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0,0,"Teste")
        col=0
        row=1
        url='https://www.uniprot.org/uniprot/P09681.txt'
        pep=content.find("Signal peptide")
        nat=content.find("Natural variant")
        pro=content.find("Propeptide")
        #if pep > 0:
        #    url_pep=""
        #    writing_col_8=worksheet.write(row,col,"Natural")
        #    table1 = soup.find('table', {'id': 'peptides_section'})
        #    headers=[]            
        #    for i in table1.find_all('th'):
        #        title=i.text
        #        headers.append(title)  
        #    mydata=pd.DataFrame(columns=headers)
        #    for j in table1.find_all('tr')[1:]:
        #        row_data = j.find_all('td')
        #        row=[i.text for i in row_data]
        #        length = len(mydata)
        #        #print(row)
        #        mydata.loc[length]=row     
        #    mydata.to_csv('a_data.csv',index=False)       
            #number=y[-6:-4]  
            #print(headers) 
        #if pro>0:
        #    url_pep=""
        #    writing_col_8=worksheet.write(row,col,"Natural")
        #    y = soup.find('a', {'title' : 'BLAST subsequence'})
        #    y=str(y)
        #    number=y[-6:-4]  
        #    row+=1   
            #print(y)         
        

    except StopIteration:
        pass  

######################################################################
######################################################################
######################################################################
######################################################################
######################################################################



##########
import os
import pandas as pd

##########



# Verifica se um arquivo existe
def fileExists(fileName):
    return os.path.isfile(fileName)

# Recebe o nome de arquivo e retorna uma lista de linhas com intervalos de classes
def filterFile(fileName):
    if not fileExists("./temp/{}".format(fileName)):
        print("File {} doesn't exist, downloading...".format(fileName))
        os.system("curl https://www.uniprot.org/uniprot/{} > ./temp/{}".format(
          fileName,
         fileName))

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

    



    planilha = open(nomePlanilha, "r")
    conteudo = planilha.readlines()
    planilha.close()
    

    #u = UniProt()
    #r=Rhea()

    #getPeptide()
    #testing_HTML()

    interval = filterFile("P09681.txt")

    print(intervalo)

    elementos = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    for elemento in elementos:
        print("Elemento: {} classificado como {}".format(elemento, classificador(elemento, intervalo)))

