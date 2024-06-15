import React from 'react'
import TestComp from './components/TestComp'

const HomePage = () => {

  /* fetch data from URL or Endpoint */
  // fetch('http://localhost:8080/api/home')
  // const testres = await fetch('http://127.0.0.1:8080/test');

  return (
    <main>
      <h1>KRISO Visualization Demo</h1>
      <TestComp />
    </main>
  )
}

export default HomePage