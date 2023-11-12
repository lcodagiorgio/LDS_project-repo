import csv
import json
import sys, getopt
import datetime
import requests


def check_if_in_list(l_item, l_list):
    """Function to check if an item is in a list.

    Args:
        l_item (list): list containing the values of a row
        l_list (list of lists): list of lists containing the values of the rows already added to the new table 

    Returns:
        int: the index of the row in the new table if the item is in the list, -1 otherwise
    """
    i = 0
    for i in range(len(l_list)):
        if l_item == l_list[i][0:len(l_item)]:
            return i
        i += 1
    return -1


def find_ind(col_names, col_of_int):
    """Function to find the indexes of the columns of interest.

    Args:
        col_names (list): list of the column names of the original table
        col_of_int (list): list of the column names of interest

    Returns:
        ind (list): list of the indexes of the columns of interest in the original table
    """
    ind = []
    for i in range(len(col_names)):
        if col_names[i] in col_of_int:
            ind.append(i)
    return ind


def write_to_csv(file, path):
    """Function to write a list of lists to a csv file.

    Args:
        file (list of list): list of lists containing the values of the rows of the new table
        path (string): path of the csv file to write
    """
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(file)


def add_crime_gravity(data, age_path="DATA//dict_participant_age.json", status_path="DATA//dict_participant_status.json", type_path="DATA//dict_participant_type.json"):
    """Function to add the crime gravity attribute to the original table.

    Args:
        data (list of lists): list of lists containing the values of the rows of the original table
        age_path (str, optional): Path of the json related to p_age. Defaults to "DATA//dict_participant_age.json".
        status_path (str, optional): Path of the json related to p_status. Defaults to "DATA//dict_participant_status.json".
        type_path (str, optional): Path of the json related to p_type. Defaults to "DATA//dict_participant_type.json".

    Returns:
        data (list of lists): list of lists containing the values of the rows of the new table
    """
    
    
    # load json file content as a dictionary
    with open(age_path) as f:
        dic_p_age = json.load(f)

    with open(status_path) as f:
        dic_p_status = json.load(f)

    with open(type_path) as f:
        dic_p_type = json.load(f)

    # define the columns of interest and find their indexes
    col_of_int = ['participant_age_group', 'participant_status', 'participant_type']
    col_id = find_ind(data[0], col_of_int)

    # add the crime gravity column to the header row
    data[0].append('crime_gravity')

    # for each row of the dataset minus the header row calculate the crime gravity index
    for obs in data[1:]:
        obs.append(dic_p_age[obs[col_id[0]]] * dic_p_status[obs[col_id[1]]] * dic_p_type[obs[col_id[2]]])

    return data


def add_unique_ids_2(data, columns, id_name='id', path = 'DATA//NEW_TAB//NEW_TAB.csv'):
    """Function that subdivides the original table into two new tables keeping lossless join

    Args:
        data (list of lists): list of lists containing the values of the rows of the original table
        columns (list): list of the columns of interest to create the new tables with 
        id_name (str, optional): the name of the newly created id column. Defaults to 'id'.
        path (str, optional): path where to create the new csv file. Defaults to 'DATA//NEW_TAB//NEW_TAB.csv'.

    Returns:
        data (list of lists): the old table without the columns of interest
        new_table (list of lists): the new table with the columns of interest and the new id column
    """
    
    # create the new table
    new_table = []
    # initialize the id counter
    id_count = 0

    # find the indexes of the columns of interest
    col_in = find_ind(data[0], columns)

    # add the new id column to the header row
    data[0].append(id_name)

    # remove the columns of interest from the header row
    for i in sorted(col_in, reverse=True):
        data[0].pop(i)
    
    # add the columns of interest and the new id column to the new table
    new_table.append(columns + [id_name])

    # initialize the dictionary that will contain the unique rows of the 
    # columns of interest as keys and the id as values
    id_dict = {}

    # for each row of the dataset minus the header row
    for row in data[1:]:
        # create a tuple with the values of the columns of interest
        new_row = tuple(row[i] for i in col_in)

        # if the tuple is not in the dictionary add it as a key and the id as value
        if new_row not in id_dict:
            id_dict[new_row] = id_count
            new_table.append(list(new_row) + [id_count])
            id_count += 1
        
        # once the tuple is in the dictionary add the id as value to the row
        row.append(id_dict[new_row])

        # remove the columns of interest from the row
        for i in sorted(col_in, reverse=True):
            row.pop(i)

    # write the new table to a csv file
    write_to_csv(new_table, path)
    
    # return the old table without the columns of interest and the new table
    return data, new_table


def quarter(year, month):
    """Function to compute the quarter the date belongs to based on the year and month.

    Args:
        year (str): the year's string representation.
        month (str): the month of the year's string representation.

    Raises:
        Exception: month must have values between 01 and 12.

    Returns:
       str: the quarter's string representation.
    """
    # casting to make sure year and month are passed as strings
    year_str = str(year)
    month_str = str(month)
    
    # defining the months belonging to each quarter
    q1 = ["01","02","03"]
    q2 = ["04","05","06"]
    q3 = ["07","08","09"]
    q4 = ["10","11","12"]
    
    # returning the correct quarter with string type
    if month_str[4:] in q1:
        return (year_str + "Q1")
    elif month_str[4:] in q2:
        return (year_str + "Q2")
    elif month_str[4:] in q3:
        return (year_str + "Q3")
    elif month_str[4:] in q4:
        return (year_str + "Q4")
    else:
        raise Exception("Month not in range 01 to 12")


def add_dates_attributes(oldDate_csv, newDate_csv):
    """Function to create a new file with needed attributes added to the original file.

    Args:
        oldDate_csv (FileDescriptorOrPath): Original file to add attributes to.
        newDate_csv (FileDescriptorOrPath): Returned file with needed attributes.
    """
    with open(oldDate_csv, "r", newline = "") as ifile:
        with open(newDate_csv, "w", newline = "") as ofile:
            dreader = csv.DictReader(ifile)
            dwriter = csv.DictWriter(ofile, fieldnames = ["date_id","date","day","month","year","quarter","weekday"])
            # writing the header of the new file
            dwriter.writeheader()
            # length of the dates without timestamps (also month and year formats)
            dateFormat = 10
            monthFormat = 7
            yearFormat = 4

            # reading every row in the input file as a dict(attName,attValue)
            for row in dreader:
                # str representation of year, month and day values
                y,m,d = tuple(row["date"][:dateFormat].split("-"))
                # extracting date from the int representation of y, m, d
                date = datetime.date(int(y),int(m),int(d))
                date_id = int(row["date_pk"])
                day = int(row["date"][:dateFormat].replace("-",""))
                month = int(row["date"][:monthFormat].replace("-",""))
                year = int(row["date"][:yearFormat].replace("-",""))
                quart = quarter(year, month)
                # retrieving the week day from the date
                weekd = date.strftime("%A")
                # composing the new dict-row to write in the output file
                newrow = {"date_id":date_id, "date":date, "day":day, "month":month, "year":year, "quarter":quart, "weekday":weekd}
                dwriter.writerow(newrow)



def clean_geo(oldGeo_csv, newGeo_csv):
    """Function to clean the geography table removing parts of or correcting values of the attributes

    Args:
        oldGeo_csv (FileDescriptorOrPath): Original file to clean attributes of.
        newGeo_csv (FileDescriptorOrPath): New file with cleaned attributes.
    """
    with open(oldGeo_csv, "r", newline = "", encoding = "cp437") as oldGeo:
        with open(newGeo_csv, "w", newline = "", encoding = "utf-8") as newGeo:
            dreader = csv.DictReader(oldGeo, delimiter=",")
            fieldnames = dreader.fieldnames
            dwriter = csv.DictWriter(newGeo, fieldnames = fieldnames, delimiter=",")
            # writing the header of the new file
            dwriter.writeheader()
            
            # reading every row in the input file as a dict(attName,attValue)
            for row in dreader:
                newrow = row.copy()
                # storing the index (if not found return -1) of the parenthesis
                ind_par = newrow["city"].find(" (")
                # replacing, if found, the in-value comma with an empty string in the attributes city and state
                newrow["city"] = newrow["city"].replace(",", "")
                newrow["state"] = newrow["state"].replace(",", "")
                # if the parenthesis is not found, write the row as it is
                if ind_par == -1:
                    dwriter.writerow(newrow)
                else:
                    # if found, write the row but with such attribute value without info in parentheses
                    newrow["city"] = newrow["city"][:ind_par]
                    dwriter.writerow(newrow)

def get_address(latitude, longitude):
    """Function to get geolocation fields from API passing latitude and longitude values

    Args:
        latitude (str|int): latitude of the location
        longitude (str|int): longitude of the location

    Returns:
        tuple(str, str, str): city, state, country
    """
    # take in input the latitude and longitude values and convert them to strings
    latitude = str(latitude)
    longitude = str(longitude)
    # API to retrieve the data needed to add the city, state and country attributes to the original file
    url = f"https://api.3geonames.org/{latitude},{longitude}.json"
    try:
        res = requests.get(url=url)
        res_json = res.json()
        # The "nearest" block contains data on the nearest locality name,
        # while "major" is for the nearest major city name.
        # They could be the same, but in large metro areas it is useful to distinguish
        # between the metro area name vs the actual suburb.
        city = res_json['major']['city']
        state = res_json['nearest']['prov']
        country = res_json['nearest']['state']
        return city, state, country
    except:
        return "Unknown", "Unknown", "Unknown"
    
def add_geo_attributes(oldGeo_csv, newGeo_csv):
    """Function to create a new file with needed attributes added to the original file.

    Args:
        oldGeo_csv (FileDescriptorOrPath): Original file to add attributes to.
        newGeo_csv (FileDescriptorOrPath): Returned file with added attributes.
    """
    with open(oldGeo_csv, "r", newline = "", encoding = "utf-8") as ifile:
        with open(newGeo_csv, "w", newline = "", encoding = "utf-8") as ofile:
            dreader = csv.DictReader(ifile)
            dwriter = csv.DictWriter(ofile, fieldnames = ["geo_id","latitude","longitude","city","state","country"])
            # writing the header of the new file
            dwriter.writeheader()

            # reading every row in the input file as a dict(attName,attValue)
            for row in dreader:
                geo_id = row["geo_id"]
                latitude = row["latitude"]
                longitude = row["longitude"]
                # unrolling the tuple with city, state and country information extracted from the json
                city, state, country = get_address(latitude, longitude)
                # composing the new dict-row to write in the output file
                newrow = {"geo_id":geo_id, "latitude":latitude, "longitude":longitude, "city":city, "state":state, "country":country}
                dwriter.writerow(newrow)


    
def add_unique_ids(data, colums, id_name='id', path = 'DATA//NEW_TAB//NEW_TAB.csv'):
    # first version of the function 
    new_table = []
    id_count = 0

    col_in = find_ind(data[0], colums)

    data[0].append(id_name)
    for i in sorted(col_in, reverse=True):
        data[0].pop(i)
        
    new_table.append(colums + [id_name])

    for row in data[1:]:
        new_row = [row[i] for i in col_in]
        ind = check_if_in_list(new_row, new_table)

        if ind == -1:
            id_count += 1
            new_row.append(id_count)
            new_table.append(new_row)
        else:
            id = new_table[ind][-1]
            new_row.append(id)

        row.append(new_row[-1])

        for i in sorted(col_in, reverse=True):
            row.pop(i)

    
    write_to_csv(new_table, path)


    return data, new_table


