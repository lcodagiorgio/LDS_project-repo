import sys, os, getopt, datetime, time
import csv, json
import requests

def get_address(latitude, longitude):
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
    # Function to create a new file with needed attributes added to the original file.
    # oldGeo_csv (FileDescriptorOrPath): Original file to add attributes to.
    # newGeo_csv (FileDescriptorOrPath): Returned file with needed attributes.
    with open(oldGeo_csv, "r", newline = "") as ifile:
        with open(newGeo_csv, "w", newline = "") as ofile:
            dreader = csv.DictReader(ifile)
            dwriter = csv.DictWriter(ofile, fieldnames = ["geo_id","latitude","longitude","city","state","country"])
            dwriter.writeheader()

            for row in dreader:
                geo_id = row["geo_id"]
                latitude = row["latitude"]
                longitude = row["longitude"]
                city, state, country = get_address(latitude, longitude)

                newrow = {"geo_id":geo_id, "latitude":latitude, "longitude":longitude, "city":city, "state":state, "country":country}
                dwriter.writerow(newrow)