import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import ImageProcessor from './components/ImageProcessor';
import HelpPage from './components/HelpPage';
import ContactPage from './components/ContactPage';
import './App.css';
import './App2.css';
import './App3.css';

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/inicio" element={<LandingPage />} />
        <Route path="/procesador" element={<ImageProcessor />} />
        <Route path="/ayuda" element={<HelpPage />} />
        <Route path="/contacto" element={<ContactPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;