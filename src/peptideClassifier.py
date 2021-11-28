# Import libraries
import os
import pandas as pd

# Import project files
import bulkDownload
from config import *


def getFileLines (fileName):
    arq = open("{}".format(fileName), "r")
    contents = arq.read()
    arq.close()
    return contents.split('\n')

#  Recebe o nome de arquivo e retorna uma lista de linhas com intervalos de classes
def getInterval (fileName):
    fileLines = getFileLines(fileName)

    preFilterLines = list(filter(lambda line: PEPTIDE_HEADER == line[:len(PEPTIDE_HEADER)], fileLines))

    partialResult = []
    for key in PEPTIDE_KEYS:
        partialResult += list(filter(lambda line: key in line, preFilterLines))

    partialResult = list(map(lambda line: line.split(), partialResult))

    finalResult = []

    for result in partialResult:
        # This also treats the case where '..' is missing in peptide interval
        begin, end = result[2].split("..") if ".." in result[2] else (result[2], result[2])

        finalResult += [[result[1],
                        int(begin) if begin.isdigit() else -1,
                        int(end) if end.isdigit() else -1]]

    return finalResult

# Classifies the protein based on the P1' position and the peptide intervals
def peptideClassifier (peptidePosition, peptideIntervals):
    # Unknown interval refers to a '?' in peptidePosition
    unknownInterval = False

    for peptideClassification, peptideBegin, peptideEnd in peptideIntervals:
        if peptideBegin == -1 or peptideEnd == -1:
            unknownInterval = True
            continue

        if peptidePosition >= peptideBegin and peptidePosition <= peptideEnd:
            return peptideClassification

    return "UNKNOWN" if unknownInterval else "OTHER"

# Generate dataframe from xlsx file
def getSheet (fileName):
    return pd.read_excel(fileName)

# Get list of all proteins
def getProteinsFromSheet (dataFrame):
    return dataFrame[HEADER_PROTEIN].tolist()

# Get the pair of Proteins with their corresponding P1' positions
def getPeptidesPositions (dataFrame):
    return dataFrame[[HEADER_PROTEIN, HEADER_P1]]

# Generate the download index from a list of desired proteins
def generateDownloadIndex (proteinList, downloadIndexFile):
    arq = open(downloadIndexFile, "w")
    arq.write("\n".join(proteinList))
    arq.close()

# Download protein files to working folder
def downloadFilesFromIndex(downloadIndexFile):
    bulkDownload.main(downloadIndexFile)

# Path to protein file
def getProteinFileName(protein):
    return TEMP_FILES_FOLDER + protein + FILE_EXTENSION

def writeResults (sheetName, dataFrame):
    dataFrame.to_excel(sheetName)


##### TO-DO: Add verbose [Info] during main code execution

def main (sheetName):
    # Load input file
    cancerCellData = getSheet(sheetName)

    # Generate proteins files index
    proteinsList = getProteinsFromSheet(cancerCellData)
    downloadIndexFile = INPUT_FILES_FOLDER + DOWNLOAD_INDEX
    generateDownloadIndex(proteinsList, downloadIndexFile)

    # Download proteins files
    downloadFilesFromIndex(downloadIndexFile)


    # Generate peptide positions
    peptidePositions = getPeptidesPositions(cancerCellData)

    
    # cancerCellData["Peptide Classification"] = peptideClassifier(peptidePositions[HEADER_P1], getInterval(getProteinFileName(peptidePositions[HEADER_PROTEIN])))
    
    # Generate new dataframe column with peptide classification
    peptideClassification = []
    for index, row in peptidePositions.iterrows():
        proteinName = row[HEADER_PROTEIN]
        peptidePosition = row[HEADER_P1]

        proteinInterval = getInterval(getProteinFileName(proteinName))

        peptideClassification += [peptideClassifier(peptidePosition, proteinInterval)]

    cancerCellData["Peptide Classification"] = peptideClassification

    writeResults(OUTPUT_FILES_FOLDER + RESULT_FILENAME_PREFIX + sheetName[sheetName.rfind("/")+1:], cancerCellData)

    ##### TO-DO: Adapt the code below to process in parallel the code above, displaying a progress bar
    ## with multiprocessing.Pool(N_CPUS) as processPool:
    ##         result = list(tqdm.tqdm(processPool.imap(download, fileList), total=len(fileList)))
    #####

if __name__ == "__main__":
    if len(os.sys.argv) != 2:
        print("[Error] Expecting 1 argument. Usage:\n\t$ python peptideClassifier.py <sheetName.xlsx>")
        os.sys.exit(1)
    sheetName = os.sys.argv[1]
    main(sheetName)