from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

import os
import pandas as pd
from datetime import datetime, timedelta
import json

from calculation import load_geojson, ship_ids, load_geojson_selected, ownship_domain

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
    'passenger': 'passenger_resample10T_ver03',
    'cargo': 'cargo_resample10T_ver03',
}

@app.route('/load_geojson_data', methods=['GET'])
def load_geojson_data():
    ship_type = request.args.get('shipType')
    datetime_str = request.args.get('datetime')
    print(f"Received ship_type: {ship_type}")
    print(f"Received datetime: {datetime_str}")
    
    ship_type = request.args.get('shipType')
    print(f"Received ship_type: {ship_type}")
    
    if not ship_type:
        return jsonify({"error": "shipType parameter is missing"}), 400

    file_name = file_mapping.get(ship_type)
    if not file_name:
        return jsonify({"error": f"No file mapping found for ship_type: {ship_type}"}), 400

    try:
        print(f"Loading file: {file_name}")
        result = load_geojson_selected(file_name, datetime_str)
        print(f"Getting ship ids Success!")
        return make_response(json.dumps(result, indent=2), 200, {'Content-Type': 'application/json'})
    
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/load_geojson_data_selected', methods=['GET'])
def load_geojson_data_selected():
    ship_type = request.args.get('shipType')
    datetime_str = request.args.get('datetime')
    print(f"Received ship_type: {ship_type}")
    print(f"Received datetime: {datetime_str}")
    
    if not ship_type:
        return jsonify({"error": "shipType parameter is missing"}), 400

    file_name = file_mapping.get(ship_type)
    if not file_name:
        return jsonify({"error": f"No file mapping found for ship_type: {ship_type}"}), 400

    try:
        print(f"Loading file: {file_name}")
        result = load_geojson_selected(file_name, datetime_str)
        print(f"Filtered data loaded successfully!")
        return make_response(json.dumps(result, indent=2), 200, {'Content-Type': 'application/json'})
    
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/get_ship_ids', methods=['GET'])
def get_ship_ids():
    ship_type = request.args.get('shipType')
    print(f"Received ship_type: {ship_type}")
    
    if not ship_type:
        return jsonify({"error": "shipType parameter is missing"}), 400

    file_name = file_mapping.get(ship_type)
    if not file_name:
        return jsonify({"error": f"No file mapping found for ship_type: {ship_type}"}), 400

    try:
        print(f"Loading file: {file_name}")
        result = ship_ids(file_name)
        print(f"Getting ship ids Success!")
        return jsonify(result)
    
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    

@app.route("/os_domain", methods=['POST'])
def os_domain():
    try:
        data = request.json
        print("Received data:", data)  # Debugging print

        ship_type = data.get('shipType')
        file_name = file_mapping.get(ship_type)
        ship_id = data.get('shipId')
        date_time = data.get('datetime')
        time_length = int(data.get('timeLength', 30))
        encounter_type = data.get('encounterType')
        print(file_name, ship_id, date_time, time_length, encounter_type)
        
        result = ownship_domain(file_name, ship_id, date_time, time_length, encounter_type)
        return make_response(json.dumps(result, indent=2), 200, {'Content-Type': 'application/json'})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400


# app running
if __name__ == "__main__":
    app.run(debug=True, port=8080) # dev mode
    # app.run() # deploy production mode