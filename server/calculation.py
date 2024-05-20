import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString
import pandas as pd
from datetime import timedelta
import math
import numpy as np
import matplotlib.pyplot as plt

# Function to read the GeoJSON file
def checkGeoJson(filename):
    # Path to the GeoJSON file
    geojson_data_path = '/data1/2024_KRISO/yykim/data_ais/' + filename + '.geojson'
    
    # Read the GeoJSON file
    try:
        gdf_geojson = gpd.read_file(geojson_data_path)
        print("GeoJSON data loaded successfully.")
        display(gdf_geojson.head())  # Display the first few rows of the GeoDataFrame
        return gdf_geojson
    except Exception as e:
        print(f"An error occurred while loading the GeoJSON data: {e}")

# Function to create circular sector
def create_sector(center, radius, start_angle, end_angle, num_points=100):
    angles = np.linspace(start_angle, end_angle, num_points)
    points = [
        Point(
            center.x + radius * math.cos(math.radians(angle)),
            center.y + radius * math.sin(math.radians(angle))
        )
        for angle in angles
    ]
    return Polygon([center] + points + [center])

# Function to calculate ships around an input ship
def calculate_ships_around(df, ship_id, recptn_dt, time_length=10):
    # Ensure RECPTN_DT is datetime
    df['RECPTN_DT'] = pd.to_datetime(df['RECPTN_DT'])
    
    print('ship id: ', ship_id)

    # Get the specific row of the input ship at the given timestamp
    ship_row = df[(df['SHIP_ID'] == ship_id) & (df['RECPTN_DT'] == recptn_dt)].iloc[0]
    ship_position = Point(ship_row['LO'], ship_row['LA'])
    sog = ship_row['SOG']
    cog = ship_row['COG']

    # Cap SOG at 102 knots if it is over 102
    if sog > 102:
        sog = 102
    
    # Calculate radius based on SOG and time length
    radius = sog * (time_length / 60)

    print('center(LO,LA): ', ship_position)
    print('radius(knot): ', radius)
    
    # Define the time window
    start_time = recptn_dt
    end_time = recptn_dt + timedelta(minutes=time_length)

    print('timeline: ', start_time, ' ~ ' , end_time)
    
    # Filter ships within the time window
    filtered_df = df[(df['RECPTN_DT'] >= start_time) & (df['RECPTN_DT'] <= end_time)]
    
    # Create 6 sectors
    sectors = []
    for i in range(6):
        start_angle = cog - 30 + i * 60
        end_angle = start_angle + 60
        sectors.append(create_sector(ship_position, radius, start_angle, end_angle))
    
    # Count ships in each sector
    result = {}
    for i, sector in enumerate(sectors):
        area_ships = filtered_df[filtered_df['geometry'].apply(lambda x: sector.contains(x))]
        unique_ships = area_ships['SHIP_ID'].unique().tolist()
        if ship_id in unique_ships:
            unique_ships.remove(ship_id)  # Remove the input ship from the list
        result[f'area{i+1}'] = {
            'count': len(unique_ships),
            'ship_ids': unique_ships
        }

    '''
    # Plot the map
    fig, ax = plt.subplots(figsize=(10, 10))
    base = df.plot(ax=ax, color='gray', markersize=5)
    for i, sector in enumerate(sectors):
        gpd.GeoSeries([sector]).plot(ax=base, color=f'C{i}', alpha=0.5, edgecolor='black')
    
    gpd.GeoSeries([ship_position]).plot(ax=base, color='red', markersize=50)
    circle = plt.Circle((ship_position.x, ship_position.y), radius, color='blue', fill=False)
    ax.add_artist(circle)
    
    # Add trace lines for detected ships
    for ship_id in filtered_df['SHIP_ID'].unique():
        ship_data = filtered_df[filtered_df['SHIP_ID'] == ship_id]
        line = LineString([(row['LO'], row['LA']) for idx, row in ship_data.iterrows()])
        gpd.GeoSeries([line]).plot(ax=base, color='black', linewidth=1)
    
    plt.title(f'Ship Collision Detection for SHIP_ID {ship_id} at {recptn_dt}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid()
    plt.show()
    '''
    
    return result