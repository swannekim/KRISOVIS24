import React from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const ShipMap = () => {
  return (
    <MapContainer center={[35.9078, 127.7669]} zoom={7} className="h-full w-full">
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      <Marker position={[35.9078, 127.7669]}>
        <Popup>
          South Korea
        </Popup>
      </Marker>
    </MapContainer>
  );
}

export default ShipMap