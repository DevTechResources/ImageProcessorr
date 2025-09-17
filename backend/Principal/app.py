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

app = Flask(__name__)
CORS(app)
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

processor = ImageProcessor()

@app.route('/api/upload', methods=['POST'])
def upload_files():
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No se encontraron archivos'}), 400
        
        files = request.files.getlist('files')
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        session_folder = os.path.join(UPLOAD_FOLDER, session_id)
        os.makedirs(session_folder, exist_ok=True)
        
        uploaded_images = []
        
        for file in files:
            if file.filename == '':
                continue
                
            filename = secure_filename(file.filename)
            file_path = os.path.join(session_folder, filename)
            file.save(file_path)
            
           
            if filename.lower().endswith('.zip'):
                
                extracted_images = processor.extract_images_from_zip(file_path, session_folder)
                for img_path in extracted_images:
                    img_info = processor.get_image_info(img_path)
                    if img_info:
                        uploaded_images.append({
                            'filename': os.path.basename(img_path),
                            'size': img_info['size'],
                            'dimensions': f"{img_info['width']}x{img_info['height']}",
                            'path': img_path
                        })
               
                os.remove(file_path)
            else:
                
                if processor.allowed_file(filename):
                    img_info = processor.get_image_info(file_path)
                    if img_info:
                        uploaded_images.append({
                            'filename': filename,
                            'size': img_info['size'],
                            'dimensions': f"{img_info['width']}x{img_info['height']}",
                            'path': file_path
                        })
        
        return jsonify({
            'session_id': session_id,
            'images': uploaded_images,
            'total_images': len(uploaded_images)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error subiendo archivos: {str(e)}'}), 500

@app.route('/api/download/<session_id>', methods=['GET'])
def download_images(session_id):
    try:
        output_folder = os.path.join(OUTPUT_FOLDER, session_id)
        
        if not os.path.exists(output_folder):
            return jsonify({'error': 'No se encontraron imágenes procesadas'}), 404
        
        processed_files = [f for f in os.listdir(output_folder) 
                          if f.endswith('.png')]
        
        if not processed_files:
            return jsonify({'error': 'No hay imágenes procesadas para descargar'}), 404
        
        if len(processed_files) == 1:
            return send_from_directory(output_folder, processed_files[0], as_attachment=True)
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename in processed_files:
                file_path = os.path.join(output_folder, filename)
                zip_file.write(file_path, filename)
        
        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'imagenes_procesadas_{session_id}.zip'
        )
        
    except Exception as e:
        return jsonify({'error': f'Error descargando: {str(e)}'}), 500

@app.route('/api/download-zip', methods=['Post'])
def home():
    return ""
       
    return "Hello, Flask!"
@app.route('/api/processor-zip', methods=['Post'])
def home():
    return ""

@app.route('/ap', methods={'Post'})
def home():
    return " "
        
if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)