import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';


export const MapComponent = () => {
  //const position = [35.9078, 127.7669]; // Coordinates for South Korea
  const position: L.LatLngExpression = [35.9078, 127.7669];

  return (
    <MapContainer center={position} zoom={8} style={{ height: '800px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={position}>
        <Popup>
          South Korea. <br /> Central coordinates.
        </Popup>
      </Marker>
    </MapContainer>
  );
};
export default MapComponent;