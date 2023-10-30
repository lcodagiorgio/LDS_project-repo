from functions_create_geography import *
import getopt, sys, os

# defining default repository paths to retrieve/store files from/to
iGeo = ".\\new_tables\\geography.csv" # input file (geography table without attributes))
oGeo = ".\\new_tables\\new_geography.csv" # output file (with attributes)

# command line execution with options ("-i" -> input file.xml, "-o" -> output file.csv)
opts, args = getopt.getopt(sys.argv[1:], "i:o:")
opts = dict(opts)

# checking if any options are passed
if len(sys.argv[1:]) > 1:
    iGeo = opts["-i"]
    oGeo = opts["-o"]

# function to add the needed attributes to the geography.csv table
add_geo_attributes(iGeo, oGeo)