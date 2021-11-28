# Import libraries
import tqdm
import requests
import os
import multiprocessing

# Configuration parameters
DEBUG = True
VERBOSE = True

TEMP_FILES_FOLDER = "./temp/"
INPUT_FILES_FOLDER = "./inputFiles/"
OUTPUT_FILES_FOLDER = "./outputFiles/"

INPUT_FILE = "proteinList.txt"

SOURCE_URL = "https://www.uniprot.org/uniprot/"

FILE_EXTENSION = ".txt"

MAXIMUM_THREADS = 32

DOWNLOAD_AGAIN = False


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

def main():
    if VERBOSE:
        print()

    # Create working folders
    createFolder(TEMP_FILES_FOLDER)
    createFolder(INPUT_FILES_FOLDER)
    createFolder(OUTPUT_FILES_FOLDER)

    # Parse input files
    proteinsFile = open(INPUT_FILES_FOLDER + INPUT_FILE, "r")
    proteins = proteinsFile.read()
    proteinsFile.close()

    fileList = ["{}{}{}".format(SOURCE_URL,
                            protein,
                            FILE_EXTENSION) for protein in proteins.split("\n")]

    # Create multiprocessing work pool
    N_CPUS = min(multiprocessing.cpu_count(), MAXIMUM_THREADS)

    if VERBOSE:
        print("[Info] System has {} CPUs, using {} CPUs for parallel work.".format(multiprocessing.cpu_count(), N_CPUS))

    if VERBOSE:
        print("[Info] Initiating file download. This may take a while.")

    with multiprocessing.Pool(N_CPUS) as processPool:
            result = list(tqdm.tqdm(processPool.imap(download, fileList), total=len(fileList)))

    if VERBOSE:
        print("[Info] File downloading complete!")

if __name__ == "__main__":
    main()
