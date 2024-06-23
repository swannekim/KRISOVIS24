'use client';
import React, { useState, useEffect, useRef } from 'react';
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
    const [encounterType, setEncounterType] = useState('');

    // Ref to prevent initial fetch on mount
    const initialRender = useRef(true);

    // Update ship IDs based on selected ship type
    useEffect(() => {
        const fetchShipIds = async () => {
            if (shipType) {
                try {
                    const response = await axios.get('http://127.0.0.1:8080/get_ship_ids', { params: { shipType } });
                    console.log("Ship IDs fetched:", response.data);  // Debugging print
                    setShipIds(response.data);
                } catch (error) {
                    console.error("Error fetching ship IDs:", error);
                }
            } else {
                setShipIds([]);
            }
        };
        if (initialRender.current) {
            initialRender.current = false;
        } else {
            fetchShipIds();
        }
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
        if (!dateTime) {
            console.error("No datetime selected.");
            return;
        }

        // Convert local datetime to UTC before sending it to the backend
        const utcDateTime = new Date(dateTime.getTime() - (dateTime.getTimezoneOffset() * 60000)).toISOString();

        try {
            const response = await axios.get('http://127.0.0.1:8080/load_geojson_data_selected', { 
                params: { 
                    shipType, 
                    datetime: utcDateTime 
                } 
            });
            console.log("fetching GeoJSON data");
            
            if (response.data) {
                setGeojsonData(response.data);  // Set the fetched GeoJSON data to state
                console.log("GeoJSON data set:");
                console.log(response.data);
            } else {
                console.log("No data received from backend.");
            }
        } catch (error) {
            console.error("Error fetching GeoJSON data:", error);
        }
    };

    const handleCalculate = async () => {
        if (!dateTime) {
            console.error("No datetime selected.");
            return;
        }

        // Convert local datetime to UTC before sending it to the backend
        const utcDateTime = new Date(dateTime.getTime() - (dateTime.getTimezoneOffset() * 60000)).toISOString();

        try {
            const response = await axios.post('http://127.0.0.1:8080/os_domain', {
                shipType,
                shipId,
                datetime: utcDateTime,
                timeLength,
                encounterType,
            });
            console.log("Calculation result:", response.data);
            setGeojsonData(response.data);
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
                    dateFormat="yyyy-MM-dd'T'HH:mm:ss"
                    className="input input-bordered input-secondary w-full"
                    placeholderText="Select Date and Time"
                />

                <button className="btn btn-primary mt-4" onClick={handleDisplay}>Display Vessels</button>
        
                <select className="select select-bordered select-secondary w-full" value={shipId} onChange={(e) => setShipId(e.target.value)}>
                    <option disabled value="">Select Ship ID</option>
                    {shipIds && shipIds.map((id) => (
                        <option key={id} value={id}>{id}</option>
                    ))}
                </select>
        
                <input
                    type="number" 
                    className="input input-bordered input-secondary w-full"
                    placeholder="Time Length (unit: 10 min)"
                    value={timeLength}
                    onChange={handleTimeLengthChange}
                />

                <select className="select select-bordered select-secondary w-full" value={encounterType} onChange={(e) => setEncounterType(e.target.value)}>
                    <option disabled value="">Select Encounter Type</option>
                    <option value="overtaking">Overtaking</option>
                    <option value="ho_crossing">Head-on & Crossing</option>
                </select>

                <button className="btn btn-primary mt-4" onClick={handleCalculate}>Check Ships Nearby</button>
            </div>
            
            <div className="w-3/4 h-[80vh] ml-4">
                <ShipMap geojsonData={geojsonData} />
            </div>
        </div>
  )
}

export default TestComp