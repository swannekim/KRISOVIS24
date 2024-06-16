import React from 'react'
import TestComp from './components/TestComp'

const HomePage = () => {

  /* fetch data from URL or Endpoint */
  // fetch('http://localhost:8080/api/home')
  // const testres = await fetch('http://127.0.0.1:8080/test');

  return (
    <div className="relative min-h-screen">
      <header className="w-full p-5 shadow-lg glass rounded-xl backdrop-blur-md bg-opacity-30 mb-4">
        <div className="container mx-auto">
          <h1 className="text-2xl font-bold">KRISO Visualization Demo</h1>
        </div>
      </header>
      <div className="flex flex-col items-center justify-center min-h-screen">
        <TestComp />
      </div>
    </div>
  )
}

export default HomePage