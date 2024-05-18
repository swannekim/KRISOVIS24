#!/bin/bash

echo "Running pickle2json for passenger_data.pickle..."
python pickle2json_edit.py passenger_data.pickle
# read -p "Check the passenger_data_edit.json file and press [Enter] to continue..."

echo "Running json2geojson for passenger_data_edit.json..."
python json2geojson_point.py passenger_data_edit.json
# read -p "Check the passenger_data_edit.geojson file and press [Enter] to continue..."

echo "Running pickle2json for cargo_data.pickle..."
python pickle2json_edit.py cargo_data.pickle
# read -p "Check the cargo_data_edit.json file and press [Enter] to continue..."

echo "Running json2geojson for cargo_data_edit.json..."
python json2geojson_point.py cargo_data_edit.json
# read -p "Check the cargo_data_edit.geojson file and press [Enter] to finish."

echo "All tasks completed."
