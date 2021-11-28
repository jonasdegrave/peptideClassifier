################################
### CONFIGURATION PARAMETERS ###
################################

# Enable/Disable messages in console: [Debug] and [Info]
DEBUG = True
VERBOSE = True

# Path to working folders
TEMP_FILES_FOLDER = "../temp/"
INPUT_FILES_FOLDER = "../inputFiles/"
OUTPUT_FILES_FOLDER = "../outputFiles/"

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

# Protein keys to look for
PEPTIDE_HEADER = "FT"
PEPTIDE_KEYS = ["SIGNAL", "PROPEP"]