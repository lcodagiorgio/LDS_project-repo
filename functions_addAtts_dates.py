import sys, getopt
import csv, json
import datetime

def quarter(year, month):
    # return the quarter based on the string slice representing the month in the chosen format
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
    year, month, day = [int(x) for x in date.split("-")]    
    ddate = datetime.date(year, month, day)
    # return string with weekday in english
    return ddate.strftime("%A")


def add_dates_attributes(oldDate_csv, newDate_csv):
    with open(oldDate_csv, "r", newline = "") as ifile:
        with open(newDate_csv, "w", newline = "") as ofile:
            dreader = csv.DictReader(ifile)
            dwriter = csv.DictWriter(ofile, fieldnames = ["date","date_pk","month","year","quarter","weekday"])
            dwriter.writeheader()
            # length of the dates without timestamps (also month and year formats)
            dateFormat = 10
            monthFormat = 7
            yearFormat = 4

            for row in dreader:
                date = row["date"][:dateFormat]
                date_pk = row["date_pk"]
                month = row["date"][:monthFormat]
                year = row["date"][:yearFormat]
                quart = quarter(year, month)
                weekd = weekday(date)

                newrow = {"date":date, "date_pk":date_pk, "month":month, "year":year, "quarter":quart, "weekday":weekd}
                dwriter.writerow(newrow)