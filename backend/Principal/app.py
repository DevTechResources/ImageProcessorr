from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import io
import zipfile
from datetime import datetime
from rembg import remove
from PIL import Image
import tempfile
import shutil
import json
from werkzeug.utils import secure_filename
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback
import oxipng

UPLOAD_FOLDER ='uploads'
OUTPUT_FOLDER ='output'
ALLOWED_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'gif', 'raw', 'webp', 'bmp',
    'tiff', 'psd', 'svg', 'eps', 'ai', 'heic', 'heif'
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


class ImageProcessor:
    def __init__(self):
        self.processing_status ={}
    
    def allowed_file(self, filename):
        return '-' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
    def extract_images_from_zip(self, zip_path, extract_to):
        extracted_images = []
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_info in zip_ref.filelist:
                    if not file_info.is_dir():
                        filename = os.path.basename(file_info.filename)
                        if self.allowed_file(filename):
                            source = zip_ref.open(file_info)
                            target_path = os.path.join(extract_to, secure_filename(filename))
                            with open(target_path, 'wb') as target:
                                shutil.copyfileobj(source, target)
                            extracted_images.append(target_path)
            return extracted_images
        except Exception as e:
            print(f"Error extrayendo ZIP: {str(e)}")
            return []   
        
    def get_image_info(self, image_path):
        try:
            with Image.open(image_path) as img:
                size = os.path.getsize(image_path)
                return {
                    'width': img.width,
                    'height': img.height,
                    'size': size,
                    'format': img.format
                }
        except Exception:
            return None
        
    def remove_background (self, input_path, output_path):
        try:
            with open(input_path, 'rb') as inp:
                background_output = remove(inp.read())
                with open(output_path, 'wb') as outp:
                    outp.write(background_output)
            return True
        except Exception as e:
            print(f"Error eliminando fondo: {str(e)}")
            return 
    
    def rezice_image(selft, input_path, output_path, width, height):
        try:
            with Image.open(input_path) as img:
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
            
                new_img = Image.new('RGBA', (int(width), int(height)), (0, 0, 0, 0))
                img.thumbnail((int(width), int(height)), Image.Resampling.LANCZOS)
                x = (int(width) - img.width) 
                y = (int(height) - img.height) 
                new_img.paste(img, (x, y), img)
                new_img.save(output_path, 'PNG', optimize=True)
            return True
        
        except Exception as e:
            print(f"Error de redimencionamiento: {str(e)}")
            return False 
    
    def optimize_image_weight(self, image_path):
        try:
            with Image.open(image_path) as img:
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                img.save(image_path, 'PNG', optimize=True, compress_level=6)
            
            oxipng(image_path, level=3)
            return True
        except Exception as e:
            print(f"Error optimizado peso: {str(e)}")
            return False
    
    def process_single_image(self, input_path, output_path):
        
        return 
    

if __name__ == '__main__':
     print(" Iniciando servidor Image Processor")
     print(" Servidor disponible en: ")
     print(" " )

    
    