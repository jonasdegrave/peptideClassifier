################################
### CONFIGURATION PARAMETERS ###
################################

# Enable/Disable messages in console: [Debug] and [Info]
DEBUG = True
VERBOSE = True

# Path to working folders
TEMP_FILES_FOLDER = "./temp/"
INPUT_FILES_FOLDER = "./inputFiles/"
OUTPUT_FILES_FOLDER = "./outputFiles/"

# TO-DO: REMOVE THIS
INPUT_FILE = "proteinList.txt"

# Source URL to download protein files from
SOURCE_URL = "https://www.uniprot.org/uniprot/"

# File extension for protein files
FILE_EXTENSION = ".txt"

# Maximum CPU threads to use in parallel downloading
MAXIMUM_THREADS = 32

# Use cached files or download everything again
DOWNLOAD_AGAIN = False