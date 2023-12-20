import csv
import math

# Define haversine function to calculate distance between two points on the hearth
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # radius of Earth in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    res = R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))
    return res

# Load data
with open('new_tables\\Geography.csv', 'r') as f:
    reader = csv.reader(f)
    df_geo = list(reader)

with open('DATA\\uscities.csv', 'r') as f:
    reader = csv.reader(f)
    df_api = list(reader)

# New list
df_geo_new = []

# Find column indices
geo_id_idx = df_geo[0].index('geo_id')
lat_geo_idx = df_geo[0].index('latitude')
lng_geo_idx = df_geo[0].index('longitude')
lat_api_idx = df_api[0].index('lat')
lng_api_idx = df_api[0].index('lng')
state_name_api_idx = df_api[0].index('state_name')
city_api_idx = df_api[0].index('city')

y = 0

for row in df_geo[1:]:  # Skip header
    y = y + 1
    # calculate distance between row and each row in df_api
    distances = [haversine(float(row[lat_geo_idx]), float(row[lng_geo_idx]), float(api_row[lat_api_idx]), float(api_row[lng_api_idx])) for api_row in df_api[1:]]
    # find index of minimum distance
    min_index = distances.index(min(distances))
    # create new row with geo_id, lat, lng, city, state, country from df_api
    new_row = [int(row[geo_id_idx]), row[lat_geo_idx], row[lng_geo_idx], df_api[min_index+1][city_api_idx], df_api[min_index+1][state_name_api_idx], 'United States']  # +1 to skip header
    # append new row to df_geo_new
    df_geo_new.append(new_row)
    # if y is multiple of 1000 print y
    if y % 100 == 0:
        print(y)
        
# col_names as first row of df_geo
col_names = df_geo[0]
# write to csv first row is col_names then each list of df_geo_new
with open('new_tables\\Geography_corr.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(col_names)
    writer.writerows(df_geo_new)