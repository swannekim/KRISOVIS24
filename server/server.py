from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

import os
import pandas as pd
from calculation import calculate_ships_around
from loaddata import load_geojson, ship_ids_list

# app instance
app = Flask(__name__)
CORS(app) # allows port 8080 in use

# app routing @ /api/home
# python3 server.py : "Hello World!" will appear on http://127.0.0.1:8080/test
@app.route("/test", methods={'GET'})
def test():
    return jsonify({
        'testmessage': "Hello World!",
        'titleofweb': "KRISO 2024 Visualization",
        'shiptype': ['cargo', 'passenger', 'tanker', 'government']
    })

file_mapping = {
    'passenger': 'passenger_data_resample10T',
    'cargo': 'cargo_data_resample10T',
}

@app.route('/geojson_loaded', methods=['GET'])
def get_geojson_loaded():
    ship_type = request.args.get('shipType')
    print(f"Received ship_type: {ship_type}")
    
    if not ship_type:
        return jsonify({"error": "shipType parameter is missing"}), 400

    file_name = file_mapping.get(ship_type)
    if not file_name:
        return jsonify({"error": f"No file mapping found for ship_type: {ship_type}"}), 400

    try:
        print(f"Loading file: {file_name}")
        geojson_data = load_geojson(file_name)
        print(f"Loading file Success!: {geojson_data}")
        return jsonify(geojson_data)
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    

@app.route("/ship_ids", methods=['GET'])
def get_ship_ids():
    try:
        ship_type = request.args.get('shipType')
        print("Received ship_type:", ship_type)  # Debugging print

        if not ship_type:
            raise ValueError("shipType parameter is required")

        geojson_filename = f"{ship_type}_data_resample10T"
        ship_ids = ship_ids_list(geojson_filename)
        return jsonify(ship_ids)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app.route("/calculate", methods=['POST'])
def calculate():
    try:
        data = request.json
        print("Received data:", data)  # Debugging print

        ship_type = data.get('shipType')
        ship_id = data.get('shipId')
        date_time = pd.to_datetime(data.get('dateTime'))
        time_length = int(data.get('timeLength', 60))
        
        geojson_filename = f"{ship_type}_data_edit"
        gdf = checkGeoJson(geojson_filename)
        
        result = calculate_ships_around(gdf, ship_id, date_time, time_length)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# app running
if __name__ == "__main__":
    app.run(debug=True, port=8080) # dev mode
    # app.run() # deploy production mode