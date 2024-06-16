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
        <div className="flex flex-row items-start justify-start min-h-screen w-full mt-4 space-x-4">
            <div className="flex flex-col space-y-4 p-4 bg-primary-content rounded-lg shadow-md z-10 relative w-1/4">
                <div className="dropdown">
                    <label tabIndex={0} className="btn btn-primary m-1">Ship Type</label>
                    <ul tabIndex={0} className="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-full z-50">
                    <li><a onClick={() => setShipType('cargo')}>Cargo</a></li>
                    <li><a onClick={() => setShipType('passenger')}>Passenger</a></li>
                    {/* Add more ship types as needed */}
                    </ul>
                </div>
        
                <div className="dropdown">
                    <label tabIndex={0} className="btn btn-primary m-1">Ship ID</label>
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
            </div>
            
            <div className="w-3/4 h-[80vh] ml-4">
                <ShipMap />
            </div>
        </div>
  )
}

export default TestComp