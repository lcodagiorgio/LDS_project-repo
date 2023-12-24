from functions_upload_tables import *
import csv
path = 'new_tables\\Geography_corr.csv'

# open path and read csv with correct data
with open(path, 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

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
    geo_id, latitude, longitude, city, state, country, lat, lng = row


    # Replace single quotes in the string values with two single quotes to escape them for SQL queries
    city = city.replace("'", "''")
    state = state.replace("'", "''")
    country = country.replace("'", "''")

    # Create the query
    query = f"""
    UPDATE Geography
    SET latitude = {latitude}, longitude = {longitude}, city = '{city}', state = '{state}', country = '{country}', city_lat = {lat}, city_lng = {lng}
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