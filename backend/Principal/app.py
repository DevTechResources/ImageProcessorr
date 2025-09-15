import os
import io
import zipfile
from datetime import datetime
from rembg import remove
from PIL import Image
import oxipng
from flask_cors import CORS

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp', 
    'raw', 'psd', 'svg', 'eps', 'ai', 'heic', 'heif'
}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)