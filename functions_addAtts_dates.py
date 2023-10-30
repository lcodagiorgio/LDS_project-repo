import sys, getopt
import csv, json
import datetime

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
    q1 = ["01","02","03"]
    q2 = ["04","05","06"]
    q3 = ["07","08","09"]
    q4 = ["10","11","12"]
    if month[5:] in q1:
        return (year + "-Q1")
    elif month[5:] in q2:
        return (year + "-Q2")
    elif month[5:] in q3:
        return (year + "-Q3")
    elif month[5:] in q4:
        return (year + "-Q4")
    else:
        raise Exception("Month not in range 01 to 12")

    
def weekday(date):
    """Function that makes use of the datetime module to find a given date's corrisponding week day.

    Args:
        date (str): The date's string representation.

    Returns:
        str: English day of the week string representation.
    """
    year, month, day = [int(x) for x in date.split("-")]    
    ddate = datetime.date(year, month, day)
    return ddate.strftime("%A")


def add_dates_attributes(oldDate_csv, newDate_csv):
    """Function to create a new file with needed attributes added to the original file.

    Args:
        oldDate_csv (FileDescriptorOrPath): Original file to add attributes to.
        newDate_csv (FileDescriptorOrPath): Returned file with needed attributes.
    """
    with open(oldDate_csv, "r", newline = "") as ifile:
        with open(newDate_csv, "w", newline = "") as ofile:
            dreader = csv.DictReader(ifile)
            dwriter = csv.DictWriter(ofile, fieldnames = ["date_id","date","month","year","quarter","weekday"])
            dwriter.writeheader()
            # length of the dates without timestamps (also month and year formats)
            dateFormat = 10
            monthFormat = 7
            yearFormat = 4

            for row in dreader:
                date = row["date"][:dateFormat]
                date_id = row["date_pk"]
                month = row["date"][:monthFormat]
                year = row["date"][:yearFormat]
                quart = quarter(year, month)
                weekd = weekday(date)

                newrow = {"date_id":date_id, "date":date, "month":month, "year":year, "quarter":quart, "weekday":weekd}
                dwriter.writerow(newrow)