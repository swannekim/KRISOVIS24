/* Display leaflet map in NextJS */
/* https://medium.com/@tomisinabiodun/displaying-a-leaflet-map-in-nextjs-85f86fccc10c */

// import React, { useEffect } from 'react';
// import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
// import 'leaflet/dist/leaflet.css';
// import "leaflet-defaulticon-compatibility";
// import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";
// import L from 'leaflet';

// interface GeoJSONFeature {
//     type: string;
//     geometry: {
//         type: string;
//         coordinates: number[] | number[][][];
//     };
//     properties: {
//         [key: string]: any;
//     };
// }

// interface GeoJSONData {
//     type: string;
//     features: GeoJSONFeature[];
// }

// interface ShipMapProps {
//     geojsonData: GeoJSONData | null;
// }

// const ShipMap: React.FC<ShipMapProps> = ({ geojsonData }) => {
//     useEffect(() => {
//         if (geojsonData) {
//             console.log("GeoJSON data received in ShipMap:", geojsonData);
//         }
//     }, [geojsonData]);

//     const onEachFeature = (feature: GeoJSONFeature, layer: L.Layer) => {
//         if (feature.properties && feature.properties.SHIP_ID) {
//             layer.bindPopup(`Ship ID: ${feature.properties.SHIP_ID}`);
//         }
//     };

//     return (
//         <MapContainer center={[35.9078, 127.7669]} zoom={6} className="h-full w-full">
//             <TileLayer
//                 url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
//                 attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
//             />
//             {geojsonData && (
//                 <GeoJSON data={geojsonData} onEachFeature={onEachFeature} />
//             )}
//         </MapContainer>
//     );
// };

// export default ShipMap;

import React, { useEffect } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import "leaflet-defaulticon-compatibility";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";
import L from 'leaflet';

interface GeoJSONFeature {
    type: string;
    geometry: {
        type: string;
        coordinates: number[] | number[][][];
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

const FeatureLayer: React.FC<{ data: GeoJSONData }> = ({ data }) => {
    const map = useMap();

    useEffect(() => {
        const onEachFeature = (feature: GeoJSONFeature, layer: L.Layer) => {
            if (feature.geometry.type === "Point") {
                const coordinates = feature.geometry.coordinates as [number, number];
                const marker = L.marker([coordinates[1], coordinates[0]]);
                marker.bindPopup(`<b>SHIP ID:</b> ${feature.properties.SHIP_ID}`);
                marker.addTo(map); // Adding marker to the map
            } else if (feature.geometry.type === "Polygon") {
                layer.bindPopup(`<b>Ellipse</b><br/><b>Angle:</b> ${feature.properties.angle}`);
            }
        };

        const geoJsonLayer = L.geoJSON(data as any, {
            onEachFeature: onEachFeature as any,
        }).addTo(map);

        return () => {
            map.removeLayer(geoJsonLayer);
        };
    }, [data, map]);

    return null;
};

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
            {geojsonData && <FeatureLayer data={geojsonData} />}
        </MapContainer>
    );
};

export default ShipMap;