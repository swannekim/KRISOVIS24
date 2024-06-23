import json
from shapely.geometry import Point, Polygon, mapping
import numpy as np
from datetime import datetime, timedelta

# Constants for conversion
METER_TO_DEGREE = 1 / 111320  # Approximation for conversion (1 degree ≈ 111.32 km)

# load_geojson('passenger_resample10T_ver03')
def load_geojson(filename):
    geojson_data_path = './testdata/' + filename + '.geojson'
    try:
        with open(geojson_data_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise ValueError(f"An error occurred while loading the GeoJSON data: {e}")

def ship_ids(filename):
    geojson_data_path = './testdata/' + filename + '.geojson'
    try:
        with open(geojson_data_path, 'r') as file:
            data = json.load(file)
            ship_ids = sorted({feature['properties']['SHIP_ID'] for feature in data['features']})
        return ship_ids
    except Exception as e:
        raise ValueError(f"An error occurred while loading the GeoJSON data and retrieving ids: {e}")

def load_geojson_selected(filename, recptn_dt_str):
    geojson_data_path = './testdata/' + filename + '.geojson'
    try:
        with open(geojson_data_path, 'r') as file:
            data = json.load(file)
            if recptn_dt_str:
                try:
                    # Remove 'Z' if it exists to match the format in your GeoJSON data
                    if recptn_dt_str.endswith('Z'):
                        recptn_dt_str = recptn_dt_str[:-5]
                    recptn_dt = datetime.fromisoformat(recptn_dt_str)
                    # Directly compare the datetime strings
                    time_filtered_features = [
                        feature for feature in data['features']
                        if datetime.fromisoformat(feature['properties']['RECPTN_DT']) == recptn_dt
                    ]
                    data['features'] = time_filtered_features
                    print(f"Filtered features count: {len(time_filtered_features)}")
                except ValueError as e:
                    raise ValueError(f"Invalid datetime format: {e}")
        return data
    except ValueError as e:
        raise ValueError(f"An error occurred while loading the GeoJSON data: {e}")
    
# Function to calculate the elliptical domain
def create_ellipse(center, semi_major, semi_minor, angle):
    ellipse = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[]]
        },
        "properties": {
            "angle": angle
        }
    }
    num_points = 100
    for i in range(num_points):
        theta = 2.0 * 3.141592653589793 * float(i) / float(num_points)
        x = semi_major * np.cos(theta)
        y = semi_minor * np.sin(theta)
        ellipse["geometry"]["coordinates"][0].append([
            center.x + x * np.cos(np.radians(angle)) - y * np.sin(np.radians(angle)),
            center.y + x * np.sin(np.radians(angle)) + y * np.cos(np.radians(angle))
        ])
    ellipse["geometry"]["coordinates"][0].append(ellipse["geometry"]["coordinates"][0][0])  # Closing the ellipse
    return ellipse

# Function to calculate ships around an input ship using Coldwell model
def ownship_domain(filename, ship_id, recptn_dt_str, time_length=30, encounter_type='ho_crossing'):
    geojson_data_path = './testdata/' + filename + '.geojson'
    try:
        with open(geojson_data_path, 'r') as file:
            geojson_data = json.load(file)
        print("GeoJSON file loaded!")

        # Remove 'Z' if it exists to match the format in your GeoJSON data
        if recptn_dt_str.endswith('Z'):
            recptn_dt_str = recptn_dt_str[:-5]
        # Parse the input datetime
        recptn_dt = datetime.fromisoformat(recptn_dt_str)
        end_time = recptn_dt + timedelta(minutes=time_length)
        print("time window: ", recptn_dt, " ~ ", end_time)
        
        # Filter the features within the time window
        time_window_features = [
            feature for feature in geojson_data['features']
            if feature['properties']['SHIP_ID'] == ship_id
            and recptn_dt <= datetime.fromisoformat(feature['properties']['RECPTN_DT']) <= end_time
        ]
        print(f"Filtered features count: {len(time_window_features)}")

        if not time_window_features:
            return {"error": f"No data found for Ship ID {ship_id} within the time window {recptn_dt} to {end_time}."}

        # Define Coldwell model dimensions
        semi_major_factor = 5 if encounter_type != 'overtaking' else 6
        semi_minor_factor = 2.5 if encounter_type != 'overtaking' else 1.75
        shift_x_factor = 0.75 if encounter_type != 'overtaking' else 0
        shift_y_factor = 1.1 if encounter_type != 'overtaking' else 0

        features = []
        
        for feature in time_window_features:
            ship_position = Point(feature['geometry']['coordinates'])
            cog = feature['properties']['COG']
            ship_length_meters = feature['properties']['LEN_PRED']
            
            # Convert ship length from meters to degrees
            ship_length_degrees = ship_length_meters * METER_TO_DEGREE
            
            # Calculate dimensions
            semi_major = semi_major_factor * ship_length_degrees
            semi_minor = semi_minor_factor * ship_length_degrees
            shift_x = shift_x_factor * ship_length_degrees
            shift_y = shift_y_factor * ship_length_degrees
            
            # Create the elliptical domain
            domain_center = Point(ship_position.x - shift_x, ship_position.y - shift_y)
            ellipse = create_ellipse(domain_center, semi_major, semi_minor, cog)
            
            # Create the vessel triangle
            # triangle = create_triangle(ship_position, ship_length_meters, cog)
            
            # Add features to the collection
            features.append(ellipse)
            #features.append(triangle)

            features.append({
                "type": "Feature",
                "geometry": mapping(ship_position),
                "properties": {
                    "SHIP_ID": ship_id,
                    "COG": cog
                }
            })
        
        # Create GeoJSON output
        output = {
            "type": "FeatureCollection",
            "features": features
        }

        return output

    except Exception as e:
        raise ValueError(f"An error occurred while loading the GeoJSON data: {e}")