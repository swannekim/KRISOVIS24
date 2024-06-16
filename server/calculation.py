import pandas as pd
import geopandas as gpd

def checkGeoJson(filename):
    geojson_data_path = '/data1/2024_KRISO/yykim/data_ais/' + filename + '.geojson'
    try:
        gdf_geojson = gpd.read_file(geojson_data_path)
        return gdf_geojson
    except Exception as e:
        raise ValueError(f"An error occurred while loading the GeoJSON data: {e}")

def get_ship_ids(filename):
    gdf = checkGeoJson(filename)
    return gdf['SHIP_ID'].unique().tolist()

def calculate_ships_around(df, ship_id, recptn_dt, time_length=60):
    df['RECPTN_DT'] = pd.to_datetime(df['RECPTN_DT'])
    
    ship_row = df[(df['SHIP_ID'] == ship_id) & (df['RECPTN_DT'] == recptn_dt)].iloc[0]
    ship_position = Point(ship_row['LO'], ship_row['LA'])
    sog = ship_row['SOG']
    cog = ship_row['COG']
    
    radius = sog * (time_length / 60)
    
    start_time = recptn_dt - timedelta(minutes=time_length / 2)
    end_time = recptn_dt + timedelta(minutes=time_length / 2)
    
    filtered_df = df[(df['RECPTN_DT'] >= start_time) & (df['RECPTN_DT'] <= end_time)]
    
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
    
    sectors = []
    for i in range(6):
        start_angle = cog - 30 + i * 60
        end_angle = start_angle + 60
        sectors.append(create_sector(ship_position, radius, start_angle, end_angle))
    
    result = {}
    for i, sector in enumerate(sectors):
        area_ships = filtered_df[filtered_df['geometry'].apply(lambda x: sector.contains(x))]
        unique_ships = area_ships['SHIP_ID'].unique()
        result[f'area{i+1}'] = {
            'count': len(unique_ships),
            'ship_ids': unique_ships.tolist()
        }
    
    return result