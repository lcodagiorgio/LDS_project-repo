from functions_xmlToCsv import *
from functions_create_table import *
import getopt, sys, os

# defining default repository paths to retrieve/store files from/to
# input file (.xml)
# output file (.csv)
iXml = ".\\DATA\\dates.xml"
oCsv = ".\\partial_tables\\new_dates.csv"
# command line execution with options ("-i" -> input file.xml, "-o" -> output file.csv)
opts, args = getopt.getopt(sys.argv[1:], "i:o:")
opts = dict(opts)

# checking if any options are passed
if len(sys.argv[1:]) > 1:
    iXml = opts["-i"]
    oCsv = opts["-o"]

# function to convert .xml to .csv
xml_to_csv(iXml, oCsv)

iCsv = oCsv
oCsv = ".\\new_tables\\Dates.csv"

# function to add the needed attributes to the obtained .csv file
add_dates_attributes(iCsv, oCsv)

# removing the temporary dates table from the repository
os.remove(".\\partial_tables\\new_dates.csv")