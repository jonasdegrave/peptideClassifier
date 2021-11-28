# Import libraries
import os
import tqdm
import requests
import multiprocessing

# Import project files
from config import *

# Verifies if a file exists;
def fileExists(fileName):
    return os.path.isfile(fileName)

# Verifies if a folder exists, if not, creates the folder;
def createFolder(folderPath):
    if not os.path.isdir(folderPath):
        if DEBUG:
            print("[Debug] Folder {} does not exist. Creating folder.".format(folderPath))
        os.mkdir(folderPath)
    else:
        if DEBUG:
            print("[Debug] Folder {} already exists. Moving on.".format(folderPath))

def download(url):
    try:
        fileName = TEMP_FILES_FOLDER + url[url.rfind("/")+1:]

        if not DOWNLOAD_AGAIN and fileExists(fileName): return

        response = requests.get(url, stream=True)
        if response.status_code == requests.codes.ok:
            with open(fileName, "wb") as file:
                for data in response:
                    file.write(data)
        else:
            print("[Error] Could not download {}. Error: {}".format(fileName, response.status_code))

    except Exception as e:
        print("[Error] {}".format(e))

def main(inputFileName):
    if VERBOSE:
        print()

    # Create working folders
    createFolder(TEMP_FILES_FOLDER)
    createFolder(INPUT_FILES_FOLDER)
    createFolder(OUTPUT_FILES_FOLDER)

    # Parse input files
    inputFile = open(inputFileName, "r")
    inputValues = inputFile.read()
    inputFile.close()

    fileList = ["{}{}{}".format(SOURCE_URL,
                            inputValue,
                            FILE_EXTENSION) for inputValue in inputValues.split("\n")]

    # Create multiprocessing work pool
    N_CPUS = min(multiprocessing.cpu_count(), MAXIMUM_THREADS)

    if VERBOSE:
        print("[Info] System has {} CPUs. Using {} CPUs for parallel work.".format(multiprocessing.cpu_count(), N_CPUS))

    if VERBOSE:
        print("[Info] Initializing bulk file download. Total of {} files in queue. This may take a while.".format(len(fileList)))

    with multiprocessing.Pool(N_CPUS) as processPool:
            result = list(tqdm.tqdm(processPool.imap(download, fileList), total=len(fileList)))

    if VERBOSE:
        print("[Info] File downloading is complete!")

if __name__ == "__main__":
    main(INPUT_FILES_FOLDER + INPUT_FILE)
