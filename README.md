# Mandaditos CDN

Un gestor de archivos CDN simple construido con Flask que permite subir, visualizar y servir archivos estáticos con generación automática de miniaturas para imágenes.

## Características

- ✨ **Subida de archivos**: Soporta múltiples formatos de imagen (PNG, JPG, JPEG, GIF, SVG, WebP)
- 🖼️ **Generación automática de miniaturas**: Crea miniaturas de 150x150px para imágenes raster
- 📁 **Gestión de archivos**: Interface web para visualizar y eliminar archivos
- 🚀 **Servicio CDN**: Endpoints dedicados para servir archivos y miniaturas
- 🐳 **Dockerizado**: Incluye configuración Docker con Nginx como proxy reverso
- 🔒 **Validación de archivos**: Solo permite formatos de imagen específicos

## Estructura del Proyecto

```
mandaditos-cdn/
├── app.py              # Aplicación principal Flask
├── requirements.txt    # Dependencias Python
├── Dockerfile         # Configuración Docker
├── nginx.conf         # Configuración Nginx
├── templates/
│   └── index.html     # Interface web principal
├── static/
│   └── style.css      # Estilos CSS
└── uploads/           # Directorio de archivos subidos
    └── thumbnails/    # Miniaturas generadas
```

## Instalación y Uso

### Opción 1: Ejecución Local

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd mandaditos-cdn
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # o
   venv\Scripts\activate     # En Windows
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**:
   ```bash
   python app.py
   ```

5. **Acceder a la aplicación**:
   Abre tu navegador en `http://localhost:5000`

### Opción 2: Docker

1. **Construir la imagen**:
   ```bash
   docker build -t mandaditos-cdn .
   ```

2. **Ejecutar el contenedor**:
   ```bash
   docker run -p 8000:8000 -v $(pwd)/uploads:/app/uploads mandaditos-cdn
   ```

3. **Acceder a la aplicación**:
   Abre tu navegador en `http://localhost:8000`

### Opción 3: Docker Compose (con Nginx)

Para un despliegue más robusto con Nginx como proxy reverso, puedes crear un `docker-compose.yml`:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app
```

## API Endpoints

### Interface Web
- `GET /` - Página principal con lista de archivos

### Gestión de Archivos
- `POST /upload` - Subir un nuevo archivo
- `POST /delete/<filename>` - Eliminar un archivo

### CDN Endpoints
- `GET /cdn/<filename>` - Servir archivo original
- `GET /cdn/thumbnails/<filename>` - Servir miniatura del archivo

## Formatos Soportados

- **PNG** (.png)
- **JPEG** (.jpg, .jpeg)
- **GIF** (.gif)
- **SVG** (.svg)
- **WebP** (.webp)

## Configuración

### Variables de Entorno (Opcionales)

- `UPLOAD_FOLDER`: Directorio para archivos subidos (default: 'uploads')
- `THUMBNAIL_FOLDER`: Directorio para miniaturas (default: 'uploads/thumbnails')
- `THUMBNAIL_SIZE`: Tamaño de miniaturas en píxeles (default: 150x150)

### Personalización

Puedes modificar las siguientes constantes en `app.py`:

```python
UPLOAD_FOLDER = 'uploads'
THUMBNAIL_FOLDER = 'uploads/thumbnails'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}
THUMBNAIL_SIZE = (150, 150)
```

## Tecnologías Utilizadas

- **Backend**: Flask 3.0.3
- **Servidor WSGI**: Gunicorn 23.0.0
- **Procesamiento de imágenes**: Pillow 10.4.0
- **Proxy reverso**: Nginx (opcional)
- **Frontend**: Bootstrap 5.3.3
- **Containerización**: Docker

## Desarrollo

### Estructura de la Aplicación

- `app.py`: Contiene toda la lógica de la aplicación Flask
- `templates/index.html`: Interface de usuario con Bootstrap
- `nginx.conf`: Configuración de Nginx para producción
- `Dockerfile`: Configuración para containerización
- `test_app.py`: Suite de pruebas unitarias e integración

### Funciones Principales

- `allowed_file()`: Valida extensiones de archivo permitidas
- `create_thumbnail()`: Genera miniaturas automáticamente
- `upload_file()`: Maneja la subida de archivos
- `delete_file()`: Elimina archivos y sus miniaturas
- `serve_file()` y `serve_thumbnail()`: Sirven archivos estáticos

### Ejecutar Tests

El proyecto incluye una suite completa de pruebas unitarias e integración:

```bash
# Usando unittest (built-in)
python test_app.py

# Usando pytest (recomendado)
pip install pytest pytest-cov
pytest test_app.py -v

# Con coverage report
pytest test_app.py --cov=app --cov-report=html
```

**Cobertura de Tests**:
- ✅ Subida de archivos (formatos válidos e inválidos)
- ✅ Generación de miniaturas
- ✅ Servicio de archivos y miniaturas
- ✅ Eliminación de archivos
- ✅ Validación de funciones helper
- ✅ Flujo completo de integración
- ✅ Manejo de errores y casos edge

## Seguridad

- ✅ Validación de tipos de archivo
- ✅ Nombres únicos para archivos (UUID)
- ✅ Sanitización de rutas de archivo
- ⚠️ **Nota**: Esta aplicación está diseñada para uso interno. Para producción, considera implementar:
  - Autenticación y autorización
  - Límites de tamaño de archivo
  - Rate limiting
  - HTTPS

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## Soporte

Si encuentras algún problema o tienes sugerencias, por favor crea un issue en el repositorio.
