'use client';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { setHours, setMinutes } from 'date-fns';

import dynamic from 'next/dynamic';

// Use dynamic import for ShipMap to disable SSR
const ShipMap = dynamic(() => import('./ShipMap'), { ssr: false });

const TestComp = () => {
    
    const [shipType, setShipType] = useState('');
    const [shipId, setShipId] = useState('');
    const [dateTime, setDateTime] = useState<Date | null>(null);
    const [timeLength, setTimeLength] = useState('');
    const [shipIds, setShipIds] = useState<string[]>([]);
    const [calculationResult, setCalculationResult] = useState(null);
    const [geojsonData, setGeojsonData] = useState<any>(null);

    // Update ship IDs based on selected ship type
    useEffect(() => {
        const fetchShipIds = async () => {
            if (shipType) {
                try {
                    const response = await axios.get('http://127.0.0.1:8080/ship_ids', { params: { shipType } });
                    console.log("Ship IDs fetched:", response.data);  // Debugging print
                    setShipIds(response.data);
                } catch (error) {
                    console.error("Error fetching ship IDs:", error);
                }
            } else {
                setShipIds([]);
            }
        };
        fetchShipIds();
    }, [shipType]);

    const handleTimeLengthChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        if (parseInt(value) > 0) {
            setTimeLength(value);
        } else {
            setTimeLength('');
        }
    };

    const handleDisplay = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8080/geojson_loaded', { params: { shipType } });
            console.log("GeoJSON data fetched:", response.data);  // Debugging print
            if (response.data) {
                setGeojsonData(response.data);  // Set the fetched GeoJSON data to state
                console.log("Set geojsonData state:", JSON.stringify(response.data, null, 2));  // Detailed log
            } else {
                console.log("No data received from backend.");  // Log if no data received
            }
        } catch (error) {
            console.error("Error fetching GeoJSON data:", error);
        }
    };

    const handleCalculate = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:8080/calculate', {
                shipType,
                shipId,
                dateTime,
                timeLength,
            });
            console.log("Calculation result:", response.data);  // Debugging print
            setCalculationResult(response.data);
        } catch (error) {
            console.error("Error calculating ships around:", error);
        }
    };


    return (
        <div className="flex flex-row items-start justify-start min-h-screen w-full mt-4 space-x-4">
            <div className="flex flex-col space-y-6 p-4 bg-primary-content rounded-lg shadow-md z-10 relative w-1/4">

                <select className="select select-bordered select-secondary w-full" value={shipType} onChange={(e) => setShipType(e.target.value)}>
                    <option disabled value="">Select Ship Type</option>
                    <option value="cargo">Cargo</option>
                    <option value="passenger">Passenger</option>
                    {/* Add more ship types as needed */}
                </select>

                <DatePicker
                    selected={dateTime}
                    onChange={(date) => setDateTime(date as Date)} // Type assertion
                    showTimeSelect
                    timeFormat="HH:mm"
                    timeIntervals={10}
                    dateFormat="MMMM d, yyyy h:mm aa"
                    className="input input-bordered input-secondary w-full"
                    placeholderText="Select Date and Time"
                />

                <button className="btn btn-primary mt-4" onClick={handleDisplay}>Display Vessels</button>
        
                <select className="select select-bordered select-secondary w-full" value={shipId} onChange={(e) => setShipId(e.target.value)}>
                    <option disabled value="">Select Ship ID</option>
                    {shipIds.map((id) => (
                        <option key={id} value={id}>{id}</option>
                    ))}
                </select>
        
                <input
                    type="number" 
                    className="input input-bordered input-secondary w-full"
                    placeholder="Time Length (minutes)"
                    value={timeLength}
                    onChange={handleTimeLengthChange}
                />

                <button className="btn btn-primary mt-4" onClick={handleCalculate}>Check Ships Nearby</button>
            </div>
            
            <div className="w-3/4 h-[80vh] ml-4">
                <ShipMap geojsonData={geojsonData} />
            </div>
        </div>
  )
}

export default TestComp