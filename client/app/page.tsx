import React from 'react'
import TestComp from './components/TestComp'

const HomePage = () => {

  /* fetch data from URL or Endpoint */
  // fetch('http://localhost:8080/api/home')
  // const testres = await fetch('http://127.0.0.1:8080/test');

  return (
    <div className="relative min-h-screen">
      <div className="absolute top-0 left-0 m-4 glass p-5 rounded-xl shadow-lg backdrop-blur-md bg-opacity-30">
        <h1 className="text-2xl font-bold">KRISO Visualization Demo</h1>
      </div>
      <div className="flex flex-col items-center justify-center min-h-screen">
        <TestComp />
      </div>
    </div>
  )
}

export default HomePage