import React from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';

import MainNavbar from './components/MainNavbar';
import BenchmarkView from './views/BenchmarkView';
import HomeView from './views/HomeView';
import PlaygroundView from './views/PlaygroundView';

import './App.css';
import './values/constants.css'
import './values/colors.css'


function App() {
  return (
    <BrowserRouter>
      <MainNavbar />
      <div className='content-view'>
        <Routes>
          <Route exact path="/" element={<HomeView />} />
          <Route path="/benchmarks" element={<BenchmarkView />} />
          <Route path="/playground" element={<PlaygroundView />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
