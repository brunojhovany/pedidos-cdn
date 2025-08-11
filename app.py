import mimetypes
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, abort
import os
import uuid
from PIL import Image, ImageOps
from werkzeug.middleware.proxy_fix import ProxyFix

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/app/content')
THUMBNAIL_FOLDER = os.getenv('THUMBNAIL_FOLDER', '/app/content/thumbnails')
PUBLIC_DNS_DOMAIN = os.getenv('PUBLIC_DNS_DOMAIN', 'localhost')
APPLICATION_ROOT = os.getenv('APPLICATION_ROOT', '/cdn/admin')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}
THUMBNAIL_SIZE = (250, 250)

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['THUMBNAIL_FOLDER'] = THUMBNAIL_FOLDER
app.config['APPLICATION_ROOT'] = APPLICATION_ROOT

# Configurar ProxyFix para manejar headers del proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.context_processor
def inject_application_root():
    return {'APPLICATION_ROOT': APPLICATION_ROOT}

mimetypes.add_type('image/webp', '.webp')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_thumbnail(image_path, thumb_path):
    try:
        img = Image.open(image_path)
        
        # Método moderno: corrige automáticamente la orientación EXIF
        img = ImageOps.exif_transpose(img)
        
        img.thumbnail(THUMBNAIL_SIZE)
        img.save(thumb_path)
        print(f"✅ Miniatura creada: {thumb_path}")
    except Exception as e:
        print(f"❌ Error creando miniatura: {e}")

def compress_and_convert_image(filepath):
    try:
        with Image.open(filepath) as img:
            # Método moderno: corrige automáticamente la orientación EXIF
            img = ImageOps.exif_transpose(img)
            
            webp_path = os.path.splitext(filepath)[0] + '.webp'
            # Guardar sin metadatos EXIF para evitar problemas futuros
            img.save(webp_path, format='WEBP', quality=80, exif=b'')
            os.remove(filepath)  # Elimina el original si se convierte
            print(f"✅ Imagen convertida a WebP: {webp_path}")
            return os.path.basename(webp_path)
    except Exception as e:
        print(f"❌ [ERROR] No se pudo comprimir/convertir la imagen: {e}")
        return None

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files = [f for f in files if f != 'thumbnails']
    return render_template('index.html', files=files, public_dns_domain=PUBLIC_DNS_DOMAIN)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4()}.{ext}"
        upload_folder_abs = os.path.abspath(app.config['UPLOAD_FOLDER'])
        filepath = os.path.normpath(os.path.join(upload_folder_abs, unique_name))
        if not filepath.startswith(upload_folder_abs):
            flash('Nombre de archivo no permitido.', 'danger')
            return redirect(url_for('index'))
        file.save(filepath)

        # Comprimir y convertir a WebP si es necesario
        if ext in ALLOWED_EXTENSIONS:
            compressed_filename = compress_and_convert_image(filepath)
            if compressed_filename:
                unique_name = compressed_filename
                filepath = os.path.join(upload_folder_abs, unique_name)
                flash(f'Imagen convertida y comprimida como {compressed_filename}.', 'success')
            else:
                flash('Error al comprimir la imagen.', 'danger')
        else:
            flash('Archivo subido sin compresión.', 'info')

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

@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
