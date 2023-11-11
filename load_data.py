from functions_load_tables import *

# Set up the connection string
server = 'tcp:lds.di.unipi.it'
database = 'Group_ID_10_DB'
username = 'Group_ID_10'
password = '6VROQBXM'
driver = '{ODBC Driver 17 for SQL Server}'

conn = connect_to_server(server, database, username, password, driver)
table_data = get_tables_col_types(conn)
print(table_data)
table_names = list(table_data.keys())

for i in range(len(table_names)):
    upload_table(table_names[i], conn, table_data[table_names[i]])
    print("Table " + table_names[i] + " uploaded")

conn.commit()
conn.close()