import { useState, useCallback } from 'react';

export const useProportionalResize = () => {
  const [width, setWidth] = useState('');
  const [height, setHeight] = useState('');
  const [originalDimensions, setOriginalDimensions] = useState(null);
  const [aspectRatio, setAspectRatio] = useState(1);
  const [isLoadingDimensions, setIsLoadingDimensions] = useState(false);

  const loadImageDimensions = useCallback(async (sessionId) => {
    if (!sessionId) return;

    setIsLoadingDimensions(true);

    try {
      const response = await fetch(`http://localhost:5000/api/dimensions/${sessionId}`);
      
      if (!response.ok) {
        throw new Error('Error obteniendo dimensiones del servidor');
      }

      const data = await response.json();
      
      if (data.success && data.dimensions) {
        const dimensions = {
          width: data.dimensions.width,
          height: data.dimensions.height,
          aspectRatio: data.dimensions.aspect_ratio,
        };
        
        setOriginalDimensions(dimensions);
        setAspectRatio(dimensions.aspectRatio);
        
        setWidth(dimensions.width.toString());
        setHeight(dimensions.height.toString());
        
        console.log(`Dimensiones cargadas: ${dimensions.width}x${dimensions.height} (ratio: ${dimensions.aspectRatio.toFixed(2)})`);
      }

    } catch (error) {
      console.error('Error obteniendo dimensiones:', error);
      const defaultDimensions = { width: 800, height: 600, aspectRatio: 800/600 };
      setOriginalDimensions(defaultDimensions);
      setAspectRatio(defaultDimensions.aspectRatio);
      setWidth('800');
      setHeight('600');
    } finally {
      setIsLoadingDimensions(false);
    }
  }, []);

  const handleWidthChange = useCallback((newWidth) => {
    setWidth(newWidth);
    
    if (newWidth && aspectRatio && !isNaN(newWidth)) {
      const numWidth = parseInt(newWidth);
      if (numWidth > 0) {
        const calculatedHeight = Math.round(numWidth / aspectRatio);
        setHeight(calculatedHeight.toString());
        console.log(`Auto-completado ancho: ${numWidth}px → ${calculatedHeight}px`);
      }
    } else if (!newWidth) {
      setHeight('');
    }
  }, [aspectRatio]);

  const handleHeightChange = useCallback((newHeight) => {
    setHeight(newHeight);
    
    if (newHeight && aspectRatio && !isNaN(newHeight)) {
      const numHeight = parseInt(newHeight);
      if (numHeight > 0) {
        const calculatedWidth = Math.round(numHeight * aspectRatio);
        setWidth(calculatedWidth.toString());
        console.log(`Auto-completado altura: ${numHeight}px → ${calculatedWidth}px`);
      }
    } else if (!newHeight) {
      setWidth('');
    }
  }, [aspectRatio]);

  const handleWidthChangeOnly = useCallback((newWidth) => {
    setWidth(newWidth);
  }, []);

  const handleHeightChangeOnly = useCallback((newHeight) => {
    setHeight(newHeight);
  }, []);

  const makeSquare = useCallback((size) => {
    const targetSize = size || parseInt(width) || parseInt(height) || 400;
    setWidth(targetSize.toString());
    setHeight(targetSize.toString());
    console.log(`Aplicado cuadrado: ${targetSize}x${targetSize}px`);
  }, [width, height]);

  const resetDimensions = useCallback(() => {
    if (originalDimensions) {
      setWidth(originalDimensions.width.toString());
      setHeight(originalDimensions.height.toString());
      console.log('Dimensiones reseteadas a originales');
    }
  }, [originalDimensions]);

  const applyPreset = useCallback((targetWidth) => {
    if (aspectRatio) {
      const calculatedHeight = Math.round(targetWidth / aspectRatio);
      setWidth(targetWidth.toString());
      setHeight(calculatedHeight.toString());
      console.log(`Preset aplicado: ${targetWidth}px → ${calculatedHeight}px`);
    }
  }, [aspectRatio]);

  const clearDimensions = useCallback(() => {
    setWidth('');
    setHeight('');
  }, []);

  return {
    width,
    height,
    originalDimensions,
    isLoadingDimensions,
    handleWidthChange,
    handleHeightChange,
    handleWidthChangeOnly,
    handleHeightChangeOnly,
    loadImageDimensions,
    makeSquare,
    resetDimensions,
    applyPreset,
    clearDimensions,
    hasValidDimensions: originalDimensions !== null,
    currentDimensions: {
      width: parseInt(width) || 0,
      height: parseInt(height) || 0
    }
  };
};