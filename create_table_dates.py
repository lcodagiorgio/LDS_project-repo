from functions_xmlToCsv import *
from functions_addAtts_dates import *
import getopt, sys, os

iXml = ".\\data\\dates.xml" # input file (.xml)
oCsv = ".\\new_tables\\new_dates.csv" # output file (.csv)

opts, args = getopt.getopt(sys.argv[1:], "i:o:")
opts = dict(opts)

iXml = opts["-i"]
oCsv = opts["-o"]

xml_to_csv(iXml, oCsv)

iCsv = oCsv
oCsv = ".\\new_tables\\dates.csv"

add_dates_attributes(iCsv, oCsv)

os.remove(".\\new_tables\\new_dates.csv")