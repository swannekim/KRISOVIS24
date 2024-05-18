"""
Pickle2JSON is a simple Python Command Line program for converting Pickle file to JSON file.
Arguments: Only one (1) argument is expected which is the pickle file.
Usage: python pickle2json_edit.py myfile.pkl
Output: The output is a JSON file bearing the same filename containing the JSON document of the converted Pickle file.
##### THIS IS EDITED VERSION #####
"""

import json
import pickle
import pandas as pd
import numpy as np
import sys
import os

# Load the pickle file
with open(sys.argv[1], 'rb') as f:
    data = pickle.load(f)

# Helper function to convert numpy types and Timestamps to Python types
def convert_types(val):
    if isinstance(val, np.generic):
        return val.item()
    elif isinstance(val, pd.Timestamp):
        return val.isoformat()  # Convert Timestamp to ISO 8601 string
    else:
        return val

json_result = []
for ship in data:
    for df in ship['SEQUENCES']:
        if 'port' not in df.columns:  # Check if 'port' column is present
            continue  # Skip processing this DataFrame if 'port' is missing

        # Assuming TYPE and TON are consistent within each DataFrame
        ship_info = {
            "SHIP_ID": ship['SHIP_ID'],
            "TYPE": df['TYPE'].iloc[0],
            "TON": df['TON'].iloc[0],
            "SEQUENCES": []
        }
        sequence_id = 1
        # Handling the 'port' column and adding sequence ID
        for df in ship['SEQUENCES']:
            if 'port' in df.columns:  # Ensure 'port' column exists before processing it
                df['SEQUENCE_ID'] = sequence_id
                df[['port_name', 'port_LA', 'port_LO']] = df['port'].str.split(',', expand=True)
                df.drop(columns='port', inplace=True)
                
                # Reset index to make sure RECPTN_DT is included in the SEQ_PROPERTIES
                df.reset_index(inplace=True)
                df.rename(columns={'index': 'RECPTN_DT'}, inplace=True)
                
                sequence_properties = df.applymap(convert_types).to_dict(orient='records')
                ship_info['SEQUENCES'].append({
                    "SEQUENCE_ID": sequence_id,
                    "SEQ_PROPERTIES": sequence_properties
                })
                sequence_id += 1
        json_result.append(ship_info)

# Write to a JSON file
output_path = os.path.splitext(sys.argv[1])[0] + '_edit.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_result, json_file, ensure_ascii=False, indent=4)

print(f'JSON: File successfully written to {output_path}')