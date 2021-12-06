import os

################################
### CONFIGURATION PARAMETERS ###
################################

# Enable/Disable messages in console: [Debug] and [Info]
DEBUG = True
VERBOSE = True

# Path to working folders
RELATIVE_PATH = ".." if ("/src" in os.getcwd()) else "."

TEMP_FILES_FOLDER = RELATIVE_PATH + "/temp/"
INPUT_FILES_FOLDER = RELATIVE_PATH + "/inputFiles/"
OUTPUT_FILES_FOLDER = RELATIVE_PATH + "/outputFiles/"

# Prefix for result filename
RESULT_FILENAME_PREFIX = "result_"

# List of protein files to download
DOWNLOAD_INDEX = "proteinList.txt"

# Source URL to download protein files from
SOURCE_URL = "https://www.uniprot.org/uniprot/"

# File extension for protein files
FILE_EXTENSION = ".txt"

# Maximum CPU threads to use in parallel downloading
MAXIMUM_THREADS = 32

# Use cached files or download everything again
DOWNLOAD_AGAIN = False

# Protein name and peptide position column headers
HEADER_PROTEIN = "protein"
HEADER_P1 = "P1' position"
HEADER_LEN_PEP="Length Pep"

# Protein keys to look for
PEPTIDE_HEADER = "FT"
PEPTIDE_KEYS = ["PEPTIDE", "SIGNAL", "PROPEP"]

PEPTIDE_COLORS = ["#1D2F6F", "#8390FA", "#6EAF46"]
#PEPTIDE_COLORS = ["#5555EE", "#444444", "#FF0000"]

PEPTIDE_OTHER = "OTHER"