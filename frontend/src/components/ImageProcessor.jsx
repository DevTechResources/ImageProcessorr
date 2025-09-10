import React, { useState, useCallback } from 'react';
import logoImage from './image/TechResources.png';

const ImageProcessor = ({ onNavigate }) => {
    
    return (
    <div className="min-h-screen app-background">
      {/* Header */}
      <header className="header">
        <div className="container header-content">
          <div className="logo-section">
            <img 
              src={logoImage}
              alt="TechRessources Logo"
              className="logo-image"
            />
          </div>
          <nav className="navigation">
            <button onClick={() => onNavigate('home')} className="nav-link nav-active">
              Inicio
            </button>
            <button onClick={() => onNavigate('procesador')} className="nav-link">
              Procesador
            </button>
            <button onClick={() => onNavigate('ayuda')} className="nav-link">
              Ayuda
            </button>
            <button onClick={() => onNavigate('contacto')} className="nav-link">
              Contacto
            </button>
          </nav>
        </div>
      </header>
      </div>
      )
};
export default ImageProcessor;