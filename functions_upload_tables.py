import pyodbc
import csv
from functions_create_table import *
def connect_to_server(server, database, username, password, driver):
    """Function to connect to the server

    Args:
        server (str): Name of the server
        database (str): Name of the database
        username (str): Username
        password (str): Password
        driver (str): Driver

    Returns:
        conn (Connection obj): Connection object from pyodbc module
    """

    # 
    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    
    # Connect to the database
    try:
        conn = pyodbc.connect(connection_string)
        print("Connection successful")
    except pyodbc.Error as e:
        print(f"Error connecting to database: {e}")


    return conn

def get_tables_col_types(conn):
    """Function to get the column names and their types of all tables in the database

    Args:
        conn (Connection obj): Connection object from pyodbc module

    Returns:
        table_data (dict): Dictionary with table names as keys and two lists one of column names and one of column types as values
    """
    # Create a cursor
    cursor = conn.cursor()

    # Get all table names with a query
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE'")
    tables = [table[0] for table in cursor.fetchall()]

    # Initialize an empty dictionary to store the table data
    table_data = {}

    # initialize a counter to skip the first table
    i = 0
    # For each table, get column names and types
    for table in tables:
        i = i + 1
        if i == 1:
            continue
        # Get column names and types with a query
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

    # Close the cursor
    cursor.close()


    return table_data


def reorder_values(col_names1, col_names2, values):
    """Function to reorder values according to a list of column names

    Args:
        col_names1 (list): list of column names in incorrect order
        col_names2 (list): list of column names in correct order
        values (list): list of values in incorrect order

    Returns:
        reordere_values (list): list of values in correct order 
    """
    # create a dictionary with the first column names as keys and the values as values
    dict_values = dict(zip(col_names1, values))
    # create a list with the values ordered as the second column names
    reordered_values = [dict_values[col_name] for col_name in col_names2]


    return reordered_values


def upload_table(table_name, conn, tab_data):
    """Function to upload a table to the database

    Args:
        table_name (str): Name of the table
        conn (Connection obj): Connection object from pyodbc module
        tab_data (list of lists): list of lists with the column names as the first elemente and types as second element
    """
    # Create a cursor
    cursor = conn.cursor()

    # Open the csv file
    with open(f"new_tables/{table_name}.csv", newline='', encoding='utf-8') as csvfile:
        # Read the csv file
        reader = csv.reader(csvfile)
        # Get the column names of the csv file
        columns_csv = next(reader)
        # Get the column names of the database table
        columns_db = tab_data[0]
        # Create a string with the column names of the database table
        columns_s = ','.join(columns_db)

        # Initialize a list to store the values strings
        values_list = []

        # Iterate over the rows of the csv file
        for row in reader:
            # Reorder the values according to the database table column names
            values = reorder_values(columns_csv, columns_db, row)
            # If the datatype is a string, formati it correctly for the SQL query
            for i in range(len(tab_data[1])):
                if tab_data[1][i] in ['nvarchar', 'date', 'char', 'varchar']:
                    values[i] = values[i].replace("'", "''")
                    values[i] = f"'{values[i]}'"
            # Add the values to the list as a unique string
            values_list.append('(' + ','.join(values) + ')')

            # If the list has 1000 values, create a query and execute it
            if len(values_list) == 1000:
                values_str = ','.join(values_list)
                query = f"INSERT INTO {table_name}({columns_s}) VALUES {values_str}"
                #print(query)
                # Execute the query
                cursor.execute(query)
                # Reset the list
                values_list = []

        # Insert remaining values if they are less than 100
        if values_list:
            values_str = ','.join(values_list)
            query = f"INSERT INTO {table_name}({columns_s}) VALUES {values_str}"
            #print(query)
            cursor.execute(query)
            
    # Close the cursor
    cursor.close()