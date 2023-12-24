from functions_upload_tables import *
import csv
path = 'new_tables\\Geography_corr.csv'
path_dat = 'DATA\\uscities.csv'

# open path and read csv with correct data
with open(path, 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# open path_dat and read csv with correct data to add zip code
with open(path_dat, 'r') as f:
    reader = csv.reader(f)
    data_dat = list(reader)

# find index for city, state, zips
for i, name in enumerate(data_dat[0]):
    if name == 'city':
        city_index = i
    elif name == 'state_name':
        state_index = i
    elif name == 'zips':
        zips_index = i

# Set up the connection string
server = 'tcp:lds.di.unipi.it'
database = 'Group_ID_10_DB'
username = 'Group_ID_10'
password = '6VROQBXM'
driver = '{ODBC Driver 17 for SQL Server}'

# Connect to the server
conn = connect_to_server(server, database, username, password, driver)

# Create a cursor
cursor = conn.cursor()

y = 0
for row in data:
    # skip the first row
    if y == 0:
        y += 1
        continue
    y += 1
    # extract values from the row
    geo_id, latitude, longitude, city, state, country = row

    # given the city and state find the postal code in data_dat
    for row_dat in data_dat:
        city_dat = row_dat[city_index]
        state_dat = row_dat[state_index]
        zips_dat = row_dat[zips_index]
        if city_dat == city and state_dat == state:
            break

    # convert zips_dat to string and take first charaters until the first space to only select first zip code
    zips_dat = str(zips_dat)
    zip_code = zips_dat[:zips_dat.find(' ')]


    # Replace single quotes in the string values with two single quotes to escape them for SQL queries
    city = city.replace("'", "''")
    state = state.replace("'", "''")
    country = country.replace("'", "''")

    # Create the query
    query = f"""
    UPDATE Geography
    SET latitude = {latitude}, longitude = {longitude}, city = '{city}', state = '{state}', country = '{country}', zip_code = '{zip_code}'
    WHERE geo_id = {geo_id}
    """

    # Execute the query
    cursor.execute(query)

    # Print the progress
    if y % 1000 == 0:
        print(y)

# Close the cursor and commit the changes
cursor.close()
conn.commit()
conn.close()