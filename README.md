# LDS_project-repo
 Repository for the Laboratory of Data Science project

create_tables.py: Creates the intial tables as csv files
create_tables_geography.py: Adds the geographycal information from the API
correct_geography.py: Changes the informations from the API using the uscities.csv file
create_tables_dates.py: Trasnforms the dates from XML to CSV format
upload_data.py: Uploads the initial version of the dataset
upload_geograpy_corrected.py: Corrects the geography data from the API with the information in the CSV

functions_create_table.py: Functions to separate the initial tables into the multiple subtables
functions_xsmToCsv.py: Functions to trasnform the dates from XML to CSV format
functions_upload_tables.py: Functions to upload the tables to the DBMS
