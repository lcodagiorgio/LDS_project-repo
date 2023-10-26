from functions_xmlToCsv import *
import getopt, sys

iXml = ".\\data\\dates.xml" # input file (.xml)
oCsv = ".\\data\\new_tab\\dates.csv" # output file (.csv)

opts, args = getopt.getopt(sys.argv[1:], "i:o:")
opts = dict(opts)

iXml = opts["-i"]
oCsv = opts["-o"]

xml_to_csv(iXml, oCsv)