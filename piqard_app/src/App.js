import React from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';

import MainNavbar from './components/MainNavbar';
import HomeView from './views/HomeView';

import './App.css';
import './values/constants.css'
import './values/colors.css'
import OpenSystemView from './views/OpenSystemView';


function App() {
  return (
    <BrowserRouter>
      <MainNavbar />
      <div className='content-view'>
        <Routes>
          <Route exact path="/" element={<HomeView />} />
          <Route path="/opensystem" element={<OpenSystemView />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
