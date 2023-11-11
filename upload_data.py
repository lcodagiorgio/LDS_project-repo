from functions_upload_tables import *

# Set up the connection string
server = 'tcp:lds.di.unipi.it'
database = 'Group_ID_10_DB'
username = 'Group_ID_10'
password = '6VROQBXM'
driver = '{ODBC Driver 17 for SQL Server}'

# Connect to the server
conn = connect_to_server(server, database, username, password, driver)

# Get information about the tables columns
table_data = get_tables_col_types(conn)
print(table_data)

# Get the names of the tables
table_names = list(table_data.keys())

# Run the queries to upload each table
for i in range(len(table_names)):
    upload_table(table_names[i], conn, table_data[table_names[i]])
    print("Table " + table_names[i] + " uploaded")

# Commit and close the connection
conn.commit()
conn.close()
