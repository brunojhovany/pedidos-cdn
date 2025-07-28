from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, abort
import os
import uuid
from PIL import Image

UPLOAD_FOLDER = 'uploads'
THUMBNAIL_FOLDER = 'uploads/thumbnails'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}
THUMBNAIL_SIZE = (150, 150)

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['THUMBNAIL_FOLDER'] = THUMBNAIL_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_thumbnail(image_path, thumb_path):
    try:
        img = Image.open(image_path)
        img.thumbnail(THUMBNAIL_SIZE)
        img.save(thumb_path)
    except Exception as e:
        print(f"Error creando miniatura: {e}")

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files = [f for f in files if f != 'thumbnails']
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        file.save(filepath)

        # Generar miniatura solo si es imagen raster (no para svg, etc.)
        if ext in {'png', 'jpg', 'jpeg', 'gif', 'webp'}:
            thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], unique_name)
            create_thumbnail(filepath, thumb_path)

        flash('Archivo subido correctamente.', 'success')
    else:
        flash('Archivo no permitido.', 'danger')
    return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    # Normalize and validate file_path
    upload_folder_abs = os.path.abspath(app.config['UPLOAD_FOLDER'])
    thumbnail_folder_abs = os.path.abspath(app.config['THUMBNAIL_FOLDER'])
    file_path = os.path.normpath(os.path.join(upload_folder_abs, filename))
    thumb_path = os.path.normpath(os.path.join(thumbnail_folder_abs, filename))

    # Ensure the paths are within the intended directories
    if not file_path.startswith(upload_folder_abs) or not thumb_path.startswith(thumbnail_folder_abs):
        flash('Nombre de archivo no permitido.', 'danger')
        return redirect(url_for('index'))

    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)

    flash('Archivo eliminado.', 'warning')
    return redirect(url_for('index'))

@app.route('/cdn/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/cdn/thumbnails/<filename>')
def serve_thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
