/* Display leaflet map in NextJS */
/* https://medium.com/@tomisinabiodun/displaying-a-leaflet-map-in-nextjs-85f86fccc10c */

import React, { useEffect } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import "leaflet-defaulticon-compatibility";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";

interface GeoJSONFeature {
    type: string;
    geometry: {
        type: string;
        coordinates: number[][][];
    };
    properties: {
        [key: string]: any;
    };
}

interface GeoJSONData {
    type: string;
    features: GeoJSONFeature[];
}

interface ShipMapProps {
    geojsonData: GeoJSONData | null;
}

const ShipMap: React.FC<ShipMapProps> = ({ geojsonData }) => {
    useEffect(() => {
        if (geojsonData) {
            console.log("GeoJSON data received in ShipMap:", geojsonData);
        }
    }, [geojsonData]);

    return (
        <MapContainer center={[35.9078, 127.7669]} zoom={6} className="h-full w-full">
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            />
            {geojsonData && (
                <GeoJSON data={geojsonData} />
            )}
        </MapContainer>
    );
};

export default ShipMap;



// import dynamic from 'next/dynamic';

// const ShipMap = dynamic(() => import('./ShipMapComponent'), { ssr: false });

// export default ShipMap;