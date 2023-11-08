from functions_create_table import *
data = []

with open('DATA//Police.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)
        
# add the crime gravity column
add_crime_gravity(data)

# Create the geograpy table 
data, geography = add_unique_ids_2(data, ["latitude", "longitude"], "geo_id", "partial_tables/geography.csv")
# Create the gun table
data, gun = add_unique_ids_2(data, ['gun_stolen','gun_type'], "gun_id", "new_tables/Gun.csv")
# Create the Partecipant table
data, partecipant = add_unique_ids_2(data, ['participant_age_group', 'participant_gender',
                                          'participant_status','participant_type',],
                                            "partecipant_id", "new_tables/Partecipant.csv")
# ceate the custody table
write_to_csv(data, "new_tables/Custody.csv")


