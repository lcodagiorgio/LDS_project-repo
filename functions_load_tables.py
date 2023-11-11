import pyodbc
import csv
from functions_create_table import *
def connect_to_server(server, database, username, password, driver):
    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    # Connect to the database
    try:
        conn = pyodbc.connect(connection_string)
        print("Connection successful")
    except pyodbc.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def get_tables_col_types(conn):
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE'")
    tables = [table[0] for table in cursor.fetchall()]

    # Initialize an empty dictionary to store the table data
    table_data = {}
    i = 0
    # For each table, get column names and types
    for table in tables:
        i = i + 1
        if i == 1:
            continue
        cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}'")
        columns = cursor.fetchall()

        # Initialize lists to store column names and types
        column_names = []
        column_types = []

        # Add column names and types to the lists
        for column in columns:
            column_names.append(column[0])
            column_types.append(column[1])

        # Add the lists to the dictionary
        table_data[table] = [column_names, column_types]

    cursor.close()
    return table_data


def reorder_values(col_names1, col_names2, values):
    # create a dictionary with the first column names as keys and the values as values
    dict_values = dict(zip(col_names1, values))
    # create a list with the values ordered as the second column names
    reordered_values = [dict_values[col_name] for col_name in col_names2]
    return reordered_values


def upload_table(table_name, conn, tab_data):
    cursor = conn.cursor()

    with open(f"new_tables/{table_name}.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        columns_csv = next(reader)
        columns_db = tab_data[0]
        columns_s = ','.join(columns_db)

        values_list = []
        for row in reader:
            values = reorder_values(columns_csv, columns_db, row)
            for i in range(len(tab_data[1])):
                if tab_data[1][i] in ['nvarchar', 'date', 'char', 'varchar']:
                    values[i] = values[i].replace("'", "''")
                    values[i] = f"'{values[i]}'"
            values_list.append('(' + ','.join(values) + ')')

            if len(values_list) == 1000:
                values_str = ','.join(values_list)
                query = f"INSERT INTO {table_name}({columns_s}) VALUES {values_str}"
                print(query)
                cursor.execute(query)
                values_list = []

        # Insert remaining values if they are less than 100
        if values_list:
            values_str = ','.join(values_list)
            query = f"INSERT INTO {table_name}({columns_s}) VALUES {values_str}"
            #print(query)
            cursor.execute(query)

    cursor.close()