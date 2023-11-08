from functions_create_table import *
import getopt, sys, os

# command line execution with options ("-i" -> input file.csv, "-o" -> output file.csv)
opts, args = getopt.getopt(sys.argv[1:], "i:o:")
opts = dict(opts)

# checking if any options are passed
if len(sys.argv[1:]) > 1:
    iGeo = opts["-i"]
    oGeo = opts["-o"]
    if opts["-t"] == "add":
        clean_geo(iGeo, oGeo)
    elif opts["-t"] == "write":
        # function to add the needed attributes to the geography.csv table
        # takes a very long time!!
        add_geo_attributes(iGeo, oGeo)

# defining default repository paths to retrieve/store files from/to
iGeo = ".\\partial_tables\\new_geography.csv" # input file (geography table without attributes))
oGeo = ".\\new_tables\\Geography.csv" # output file (with attributes)
clean_geo(iGeo, oGeo) # by default, only clean the attributes