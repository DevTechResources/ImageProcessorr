import React, { useState } from 'react';
import logoImage from './image/TechResources.png';

const HelpPage = ({ onNavigate }) => {
 
  return (
     <div className="min-h-screen app-background">
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
    
      <div className="main-containerHelp">
        <div className="containerHelp">
        <div className='logoImageProcessor'>
            <h3>ImageProcessor</h3> 
          <div className="help-header">
            <h1>Centro de Ayuda </h1>
            <p>Encuentra toda la información que necesitas para sacar el máximo provecho de ImageProcessor</p>
          </div>
        </div>   
        </div>
      </div>

        <div>
            <p>Navegación </p>
            <li>
            <button>Primeros Pasos</button>
            </li>
            <li>
            <button>Funcionalidades</button>
            </li>
            <li>
            <button>Formatos Soportados</button>
            </li>
            <li>
            <button>Preguntas Frecuentes</button>
            </li>
            <li>
            <button>Solución de Problemas</button>
            </li>
            <li>
            <button>Consejos y Trucos</button>
            </li>     
        </div>
</div>
  );
};

export default HelpPage;