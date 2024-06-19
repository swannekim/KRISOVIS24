import React from 'react';
import { MapContainer, TileLayer, GeoJSON, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import "leaflet-defaulticon-compatibility";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";

interface ShipMapComponentProps {
    geojsonData: any; // You can replace 'any' with a more specific type if you have one
}

const ShipMapComponent: React.FC<ShipMapComponentProps> = ({ geojsonData }) => {
    console.log("GeoJSON data received in ShipMapComponent:", geojsonData);

    const getMarkers = () => {
        if (!geojsonData || !geojsonData.features) {
            console.log("No GeoJSON data or features found.");  // Debugging print
            return [];
        }

        return geojsonData.features.map((feature: any, index: number) => {
            const [lon, lat] = feature.geometry.coordinates;
            const { SHIP_ID, RECPTN_DT, TYPE } = feature.properties;
            console.log("Creating marker for:", SHIP_ID, lat, lon);  // Debugging print

            return (
                <Marker key={index} position={[lat, lon]}>
                    <Popup>
                        <div>
                            <strong>Ship ID:</strong> {SHIP_ID}<br />
                            <strong>Type:</strong> {TYPE}<br />
                            <strong>Received at:</strong> {RECPTN_DT}
                        </div>
                    </Popup>
                </Marker>
            );
        });
    };

    return (
        <MapContainer center={[35.9078, 127.7669]} zoom={6} className="h-full w-full">
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />

            {geojsonData && (
                <GeoJSON data={geojsonData} />
            )}
            {getMarkers()}

            <Marker position={[35.9078, 127.7669]}>
                <Popup>
                South Korea
                </Popup>
            </Marker>
        </MapContainer>
    );
}

export default ShipMapComponent;