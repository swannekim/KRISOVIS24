## GeoJSON file

- data location: ~/KRISO_VIS/KRISOVIS24/server/testdata/
  - data copied to public folder with following command: cp ~/KRISO_VIS/KRISOVIS24/server/testdata/passenger_resample10T_ver03.geojson /data1/2024_KRISO/yykim/data_ais/


- example shape:

```
{'type': 'FeatureCollection',
 'features': [{'type': 'Feature',
   'properties': {'SHIP_ID': '123456788',
    'RECPTN_DT': '2022-08-12T01:30:00',
    'SEQUENCE_ID': 1,
    'SOG': 10.7,
    'COG': 96.8,
    'TYPE': 'passenger',
    'LEN_PRED': 6.25,
    'TON': 11.0,
    'dist': 148.67964567511444,
    'sea_lv': 182.0,
    'port_name': '이어도',
    'port_geometry': {'type': 'Point', 'coordinates': [125.16667, 32.11667]}},
   'geometry': {'type': 'Point', 'coordinates': [126.542485, 31.468265]}},
  {'type': 'Feature',
   'properties': {'SHIP_ID': '123456788',
    'RECPTN_DT': '2022-08-24T22:00:00',
    'SEQUENCE_ID': 2,
    'SOG': 5.3,
    'COG': 60.5,
    'TYPE': 'passenger',
    'LEN_PRED': 6.25,
    'TON': 11.0,
    'dist': 133.91085080078506,
...
    'port_name': '도농탄',
    'port_geometry': {'type': 'Point', 'coordinates': [126.26667, 33.15]}},
   'geometry': {'type': 'Point',
    'coordinates': [126.99159285714286, 31.731724047619043]}},
  ...]}
  ```