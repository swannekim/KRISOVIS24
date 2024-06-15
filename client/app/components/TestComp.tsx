'use client';
import React, { useState, useEffect } from 'react';
import ShipMap from './ShipMap'

const TestComp = () => {
    
    const [shipType, setShipType] = useState('');
    const [shipId, setShipId] = useState('');
    const [dateTime, setDateTime] = useState('');
    const [timeLength, setTimeLength] = useState('');
    const [shipIds, setShipIds] = useState<string[]>([]);

    // Update ship IDs based on selected ship type
    useEffect(() => {
        if (shipType) {
        setShipIds(shipData[shipType] || []);
        } else {
        setShipIds([]);
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

    return (
        <div className="flex flex-col items-center justify-center min-h-screen space-y-4">
            <div className="w-full flex justify-start p-4 space-x-4">
            <div className="dropdown">
                <label tabIndex={0} className="btn btn-primary m-1">Ship Type</label>
                <ul tabIndex={0} className="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
                <li><a onClick={() => setShipType('cargo')}>Cargo</a></li>
                <li><a onClick={() => setShipType('passenger')}>Passenger</a></li>
                {/* Add more ship types as needed */}
                </ul>
            </div>
    
            <div className="dropdown">
                <label tabIndex={0} className="btn btn-primary m-1">Ship ID</label>
                <ul tabIndex={0} className="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
                {shipIds.map((id) => (
                    <li key={id}><a onClick={() => setShipId(id)}>{id}</a></li>
                ))}
                </ul>
            </div>
    
            <input 
                type="datetime-local" 
                className="input input-bordered w-48"
                value={dateTime}
                onChange={(e) => setDateTime(e.target.value)}
            />
    
            <input 
                type="number" 
                className="input input-bordered w-48"
                placeholder="Time Length (minutes)"
                value={timeLength}
                onChange={handleTimeLengthChange}
            />
            </div>
            
            <div className="w-full h-96">
            <ShipMap />
            </div>
        </div>
  )
}

export default TestComp