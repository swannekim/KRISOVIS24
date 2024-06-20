import json
import pandas as pd
import geopandas as gpd
import numpy as np
from tqdm import tqdm

# Load the vessel_static.csv data
vessel_static = pd.read_csv('vessel_static.csv')

def load_geojson(filename):
    geojson_data_path = '../server/testdata/' + filename + '.geojson'
    try:
        with open(geojson_data_path, 'r') as file:
            data = json.load(file)
        print("GeoJSON data loaded successfully.")
        return data
    except Exception as e:
        raise ValueError(f"An error occurred while loading the GeoJSON data: {e}")
    
def load_geojson_gpd(filename):
    # Path to the GeoJSON file
    geojson_data_path = '../server/testdata/' + filename + '.geojson'

    # Read the GeoJSON file
    try:
        gdf_geojson = gpd.read_file(geojson_data_path)
        print("GeoJSON data loaded successfully.")
        return gdf_geojson
    
    except Exception as e:
        print(f"An error occurred while loading the GeoJSON data: {e}")

myjsonfile2 = load_geojson('passenger_data_resample10T_ver02')
mygdffile2 = load_geojson_gpd('passenger_data_resample10T_ver02')


# Define the function to predict the length
def predict_length(ship_type, ton):
    # Filter the vessel_static data to match the ship type (case-insensitive)
    type_filtered = vessel_static[vessel_static['shiptype'].str.contains(ship_type, case=False, na=False)]

    if not type_filtered.empty:
        # Filter to match the TON
        ton_filtered = type_filtered[type_filtered['ton'] == ton]

        if not ton_filtered.empty:
            # If exact match, return the median length
            return ton_filtered['length'].median()
        else:
            # If no exact match, perform linear interpolation
            sorted_filtered = type_filtered.sort_values(by='ton')

            # Group by 'ton' and get the median length for interpolation
            grouped_median = sorted_filtered.groupby('ton')['length'].median().reset_index()

            # Find the closest values for interpolation
            lower_bound = grouped_median[grouped_median['ton'] <= ton].tail(1)
            upper_bound = grouped_median[grouped_median['ton'] >= ton].head(1)

            if not lower_bound.empty and not upper_bound.empty:
                if lower_bound['ton'].values[0] == upper_bound['ton'].values[0]:
                    return lower_bound['length'].values[0]
                else:
                    # Perform linear interpolation
                    x0, y0 = lower_bound['ton'].values[0], lower_bound['length'].values[0]
                    x1, y1 = upper_bound['ton'].values[0], upper_bound['length'].values[0]
                    return y0 + (ton - x0) * (y1 - y0) / (x1 - x0)
            elif not lower_bound.empty:
                return lower_bound['length'].values[0]
            elif not upper_bound.empty:
                return upper_bound['length'].values[0]
            else:
                return np.nan
    else:
        return np.nan

def predict_length_mapping(geojson_data, output_filename):
    # Add the LEN_PRED feature to each feature in the GeoJSON data with progress bar
    for feature in tqdm(geojson_data['features'], desc="Processing features"):
        properties = feature['properties']
        ship_type = properties['TYPE']
        ton = properties['TON']

        # Predict the length
        len_pred = predict_length(ship_type, ton)

        # Insert LEN_PRED into properties dictionary
        properties['LEN_PRED'] = len_pred

        # Reorder properties to insert LEN_PRED after TON
        ordered_properties = {k: properties[k] for k in list(properties)[:6]}
        ordered_properties['LEN_PRED'] = len_pred
        for k in list(properties)[6:]:
            ordered_properties[k] = properties[k]

        feature['properties'] = ordered_properties

    # Save the modified GeoJSON data to a new file
    output_geojson_path = '../server/testdata/' + output_filename + '.geojson'
    with open(output_geojson_path, 'w') as outfile:
        json.dump(geojson_data, outfile, indent=4)

    print(f"Transformed GeoJSON data with LEN_PRED saved successfully to {output_geojson_path}")

# Run the function with progress logging
predict_length_mapping(myjsonfile2, 'passenger_resample10T_ver03')