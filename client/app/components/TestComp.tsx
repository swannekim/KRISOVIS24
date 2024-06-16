'use client';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

import ShipMap from './ShipMap'

const TestComp = () => {
    
    const [shipType, setShipType] = useState('');
    const [shipId, setShipId] = useState('');
    const [dateTime, setDateTime] = useState('');
    const [timeLength, setTimeLength] = useState('');
    const [shipIds, setShipIds] = useState<string[]>([]);
    const [calculationResult, setCalculationResult] = useState(null);

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
            <div className="flex flex-col space-y-5 p-4 bg-primary-content rounded-lg shadow-md z-10 relative w-1/4">
                <div className="dropdown">
                    <label tabIndex={0} className="btn btn-secondary m-1">Ship Type</label>
                    <ul tabIndex={0} className="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-full z-50">
                    <li><a onClick={() => setShipType('cargo')}>Cargo</a></li>
                    <li><a onClick={() => setShipType('passenger')}>Passenger</a></li>
                    {/* Add more ship types as needed */}
                    </ul>
                </div>
        
                <div className="dropdown">
                    <label tabIndex={0} className="btn btn-secondary m-1">Ship ID</label>
                    <ul tabIndex={0} className="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-full z-50">
                    {shipIds.map((id) => (
                        <li key={id}><a onClick={() => setShipId(id)}>{id}</a></li>
                    ))}
                    </ul>
                </div>
        
                <input 
                    type="datetime-local" 
                    className="input input-bordered w-full"
                    value={dateTime}
                    onChange={(e) => setDateTime(e.target.value)}
                />
        
                <input 
                    type="number" 
                    className="input input-bordered w-full"
                    placeholder="Time Length (minutes)"
                    value={timeLength}
                    onChange={handleTimeLengthChange}
                />

                <button className="btn btn-primary mt-4" onClick={handleCalculate}>Check Ships Nearby</button>
            </div>
            
            <div className="w-3/4 h-[80vh] ml-4">
                <ShipMap />
            </div>
        </div>
  )
}

export default TestComp