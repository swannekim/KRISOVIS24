# loaddata.py

import json

def load_geojson(filename):
    geojson_data_path = './testdata/' + filename + '.geojson'
    try:
        with open(geojson_data_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise ValueError(f"An error occurred while loading the GeoJSON data: {e}")

def ship_ids_list(filename):
    data = load_geojson(filename)
    ship_ids = {feature['properties']['SHIP_ID'] for feature in data['features']}
    return list(ship_ids)
