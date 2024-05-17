"""
Pickle2JSON is a simple Python Command Line program for converting Pickle file to JSON file.
Arguments: Only one (1) argument is expected which is the pickle file.
Usage: python json2geojson_point.py myfile.json
Output: The output is a JSON file bearing the same filename containing the JSON document of the converted Pickle file.
##### THIS IS EDITED VERSION #####
"""

import json
import sys
import os

# Read the original JSON data
with open(sys.argv[1], 'r') as file:
    json_data = json.load(file)

# Initialize the GeoJSON structure
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Traverse each ship and each sequence and each property set within the sequence
for ship in json_data:
    ship_id = ship['SHIP_ID']
    for sequence in ship['SEQUENCES']:
        for prop in sequence['SEQ_PROPERTIES']:
            # Create a GeoJSON feature for each property set
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [prop['port_LO'], prop['port_LA']]
                },
                "properties": {
                    "SHIP_ID": ship_id,
                    "SEQUENCE_ID": sequence['SEQUENCE_ID'],
                    **{key: value for key, value in prop.items() if key not in ['port_LA', 'port_LO']}
                }
            }
            geojson['features'].append(feature)

# Save the GeoJSON data to a new file
output_path = os.path.splitext(sys.argv[1])[0] + '.geojson'
with open(output_path, 'w') as file:
    json.dump(geojson, file, ensure_ascii=False, indent=4)

print(f'GeoJSON data has been written to {output_path}')