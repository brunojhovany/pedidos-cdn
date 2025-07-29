import unittest
import tempfile
import os
import shutil
from io import BytesIO
from PIL import Image
import uuid
from app import app

class MandaditosCDNTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        # Create temporary directories for testing
        self.test_dir = tempfile.mkdtemp()
        self.upload_dir = os.path.join(self.test_dir, 'uploads')
        self.thumbnail_dir = os.path.join(self.test_dir, 'uploads', 'thumbnails')
        
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.thumbnail_dir, exist_ok=True)
        
        self.app.config['UPLOAD_FOLDER'] = self.upload_dir
        self.app.config['THUMBNAIL_FOLDER'] = self.thumbnail_dir
        
        self.client = self.app.test_client()
        
    def tearDown(self):
        """Clean up after each test method."""
        shutil.rmtree(self.test_dir)
    
    def create_test_image(self, format='JPEG', size=(100, 100)):
        """Create a test image in memory."""
        img = Image.new('RGB', size, color='red')
        img_io = BytesIO()
        img.save(img_io, format=format)
        img_io.seek(0)
        return img_io
    
    def test_index_page_loads(self):
        """Test that the main page loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Gestor de Archivos CDN', response.data)
        self.assertIn(b'Subir archivo', response.data)
    
    def test_index_shows_uploaded_files(self):
        """Test that uploaded files are displayed on the main page."""
        # Create a test file in the upload directory
        test_filename = 'test_image.jpg'
        test_file_path = os.path.join(self.upload_dir, test_filename)
        
        # Create a simple test file
        with open(test_file_path, 'w') as f:
            f.write('test content')
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_filename.encode(), response.data)
    
    def test_upload_valid_image(self):
        """Test uploading a valid image file."""
        img_data = self.create_test_image()
        
        response = self.client.post('/upload', data={
            'file': (img_data, 'test_image.jpg')
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Archivo subido correctamente', response.data)
        
        # Check if file was saved (should have UUID name)
        uploaded_files = os.listdir(self.upload_dir)
        uploaded_files = [f for f in uploaded_files if f != 'thumbnails']
        self.assertEqual(len(uploaded_files), 1)
        self.assertTrue(uploaded_files[0].endswith('.webp'))  # Assuming conversion to WebP
    
    def test_upload_creates_thumbnail(self):
        """Test that uploading an image creates a thumbnail."""
        img_data = self.create_test_image()
        
        response = self.client.post('/upload', data={
            'file': (img_data, 'test_image.jpg')
        })
        
        # Check if thumbnail was created
        thumbnails = os.listdir(self.thumbnail_dir)
        self.assertEqual(len(thumbnails), 1)
        self.assertTrue(thumbnails[0].endswith('.webp'))  # Assuming thumbnails are saved as WebP
    
    def test_upload_png_image(self):
        """Test uploading a PNG image."""
        img_data = self.create_test_image(format='PNG')
        
        response = self.client.post('/upload', data={
            'file': (img_data, 'test_image.png')
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Archivo subido correctamente', response.data)
        
        uploaded_files = os.listdir(self.upload_dir)
        uploaded_files = [f for f in uploaded_files if f != 'thumbnails']
        self.assertEqual(len(uploaded_files), 1)
        self.assertTrue(uploaded_files[0].endswith('.webp'))
    
    def test_upload_webp_image(self):
        """Test uploading a WebP image."""
        img_data = self.create_test_image(format='WEBP')
        
        response = self.client.post('/upload', data={
            'file': (img_data, 'test_image.webp')
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Archivo subido correctamente', response.data)
    
    def test_upload_invalid_file_extension(self):
        """Test uploading a file with invalid extension."""
        # Create a fake text file
        fake_file = BytesIO(b'This is not an image')
        
        response = self.client.post('/upload', data={
            'file': (fake_file, 'test_file.txt')
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Archivo no permitido', response.data)
        
        # Check that no file was uploaded
        uploaded_files = os.listdir(self.upload_dir)
        uploaded_files = [f for f in uploaded_files if f != 'thumbnails']
        self.assertEqual(len(uploaded_files), 0)
    
    def test_upload_no_file(self):
        """Test uploading without selecting a file."""
        response = self.client.post('/upload', data={})
        
        # Should redirect back to main page
        self.assertEqual(response.status_code, 302)
    
    def test_delete_file(self):
        """Test deleting an uploaded file."""
        # First upload a file
        img_data = self.create_test_image()
        self.client.post('/upload', data={
            'file': (img_data, 'test_image.jpg')
        })
        
        # Get the uploaded filename
        uploaded_files = os.listdir(self.upload_dir)
        uploaded_files = [f for f in uploaded_files if f != 'thumbnails']
        filename = uploaded_files[0]
        
        # Delete the file
        response = self.client.post(f'/delete/{filename}', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Archivo eliminado', response.data)
        
        # Check that file and thumbnail were deleted
        remaining_files = os.listdir(self.upload_dir)
        remaining_files = [f for f in remaining_files if f != 'thumbnails']
        self.assertEqual(len(remaining_files), 0)
        
        remaining_thumbnails = os.listdir(self.thumbnail_dir)
        self.assertEqual(len(remaining_thumbnails), 0)
    
    def test_delete_nonexistent_file(self):
        """Test deleting a file that doesn't exist."""
        response = self.client.post('/delete/nonexistent.jpg', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Archivo eliminado', response.data)
    
    def test_serve_file(self):
        """Test serving an uploaded file."""
        # Create a test file directly
        test_filename = f'{uuid.uuid4()}.jpg'
        test_file_path = os.path.join(self.upload_dir, test_filename)
        
        img = Image.new('RGB', (50, 50), color='blue')
        img.save(test_file_path, 'JPEG')
        
        response = self.client.get(f'/cdn/{test_filename}')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'image/jpeg')
    
    def test_serve_thumbnail(self):
        """Test serving a thumbnail."""
        # Create a test thumbnail directly
        test_filename = f'{uuid.uuid4()}.jpg'
        test_thumb_path = os.path.join(self.thumbnail_dir, test_filename)
        
        img = Image.new('RGB', (150, 150), color='green')
        img.save(test_thumb_path, 'JPEG')
        
        response = self.client.get(f'/cdn/thumbnails/{test_filename}')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'image/jpeg')
    
    def test_serve_nonexistent_file(self):
        """Test serving a file that doesn't exist."""
        response = self.client.get('/cdn/nonexistent.jpg')
        self.assertEqual(response.status_code, 404)
    
    def test_serve_nonexistent_thumbnail(self):
        """Test serving a thumbnail that doesn't exist."""
        response = self.client.get('/cdn/thumbnails/nonexistent.jpg')
        self.assertEqual(response.status_code, 404)
    
    def test_allowed_file_function(self):
        """Test the allowed_file helper function."""
        from app import allowed_file
        
        # Test valid extensions
        self.assertTrue(allowed_file('image.jpg'))
        self.assertTrue(allowed_file('image.jpeg'))
        self.assertTrue(allowed_file('image.png'))
        self.assertTrue(allowed_file('image.gif'))
        self.assertTrue(allowed_file('image.svg'))
        self.assertTrue(allowed_file('image.webp'))
        
        # Test invalid extensions
        self.assertFalse(allowed_file('document.txt'))
        self.assertFalse(allowed_file('document.pdf'))
        self.assertFalse(allowed_file('script.py'))
        self.assertFalse(allowed_file('noextension'))
        
        # Test case insensitivity
        self.assertTrue(allowed_file('image.JPG'))
        self.assertTrue(allowed_file('image.PNG'))
    
    def test_create_thumbnail_function(self):
        """Test the create_thumbnail helper function."""
        from app import create_thumbnail
        
        # Create a test image
        test_image_path = os.path.join(self.upload_dir, 'test.jpg')
        img = Image.new('RGB', (500, 500), color='red')
        img.save(test_image_path, 'JPEG')
        
        # Create thumbnail
        thumb_path = os.path.join(self.thumbnail_dir, 'test.jpg')
        create_thumbnail(test_image_path, thumb_path)
        
        # Check if thumbnail was created and has correct size
        self.assertTrue(os.path.exists(thumb_path))
        
        thumb_img = Image.open(thumb_path)
        self.assertLessEqual(thumb_img.width, 150)
        self.assertLessEqual(thumb_img.height, 150)
    
    def test_multiple_file_uploads(self):
        """Test uploading multiple files."""
        # Upload first file
        img_data1 = self.create_test_image()
        self.client.post('/upload', data={
            'file': (img_data1, 'test_image1.jpg')
        })
        
        # Upload second file
        img_data2 = self.create_test_image()
        self.client.post('/upload', data={
            'file': (img_data2, 'test_image2.png')
        })
        
        # Check both files are uploaded
        uploaded_files = os.listdir(self.upload_dir)
        uploaded_files = [f for f in uploaded_files if f != 'thumbnails']
        self.assertEqual(len(uploaded_files), 2)
        
        # Check both thumbnails are created
        thumbnails = os.listdir(self.thumbnail_dir)
        self.assertEqual(len(thumbnails), 2)
    
    def test_uuid_filename_generation(self):
        """Test that uploaded files get UUID names."""
        img_data = self.create_test_image()
        
        response = self.client.post('/upload', data={
            'file': (img_data, 'original_name.jpg')
        })
        
        uploaded_files = os.listdir(self.upload_dir)
        uploaded_files = [f for f in uploaded_files if f != 'thumbnails']
        filename = uploaded_files[0]
        
        # Check that filename is a UUID (should not be original name)
        self.assertNotEqual(filename, 'original_name.jpg')
        self.assertTrue(filename.endswith('.webp'))  # Assuming conversion to WebP
        
        # Try to parse as UUID (will raise ValueError if not valid UUID)
        try:
            uuid.UUID(filename.rsplit('.', 1)[0])
        except ValueError:
            self.fail("Generated filename is not a valid UUID")


class MandaditosCDNIntegrationTest(unittest.TestCase):
    """Integration tests for the complete workflow."""
    
    def setUp(self):
        """Set up test fixtures for integration tests."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.test_dir = tempfile.mkdtemp()
        self.upload_dir = os.path.join(self.test_dir, 'uploads')
        self.thumbnail_dir = os.path.join(self.test_dir, 'uploads', 'thumbnails')
        
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.thumbnail_dir, exist_ok=True)
        
        self.app.config['UPLOAD_FOLDER'] = self.upload_dir
        self.app.config['THUMBNAIL_FOLDER'] = self.thumbnail_dir
        
        self.client = self.app.test_client()
    
    def tearDown(self):
        """Clean up after integration tests."""
        shutil.rmtree(self.test_dir)
    
    def create_test_image(self, format='JPEG', size=(200, 200)):
        """Create a test image for integration tests."""
        img = Image.new('RGB', size, color='blue')
        img_io = BytesIO()
        img.save(img_io, format=format)
        img_io.seek(0)
        return img_io
    
    def test_complete_workflow(self):
        """Test the complete upload -> serve -> delete workflow."""
        # 1. Upload an image
        img_data = self.create_test_image()
        upload_response = self.client.post('/upload', data={
            'file': (img_data, 'workflow_test.jpg')
        }, follow_redirects=True)
        
        self.assertEqual(upload_response.status_code, 200)
        self.assertIn(b'Archivo subido correctamente', upload_response.data)
        
        # 2. Get the uploaded filename
        uploaded_files = os.listdir(self.upload_dir)
        uploaded_files = [f for f in uploaded_files if f != 'thumbnails']
        self.assertEqual(len(uploaded_files), 1)
        filename = uploaded_files[0]
        
        # 3. Serve the original file
        serve_response = self.client.get(f'/cdn/{filename}')
        self.assertEqual(serve_response.status_code, 200)
        # expect a webp file
        self.assertEqual(serve_response.content_type, 'image/webp')
        
        # 4. Serve the thumbnail
        thumb_response = self.client.get(f'/cdn/thumbnails/{filename}')
        self.assertEqual(thumb_response.status_code, 200)
        self.assertEqual(thumb_response.content_type, 'image/webp')
        
        # 5. Check that file appears on main page
        index_response = self.client.get('/')
        self.assertEqual(index_response.status_code, 200)
        self.assertIn(filename.encode(), index_response.data)
        
        # 6. Delete the file
        delete_response = self.client.post(f'/delete/{filename}', follow_redirects=True)
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn(b'Archivo eliminado', delete_response.data)
        
        # 7. Verify file is no longer accessible
        serve_after_delete = self.client.get(f'/cdn/{filename}')
        self.assertEqual(serve_after_delete.status_code, 404)
        
        thumb_after_delete = self.client.get(f'/cdn/thumbnails/{filename}')
        self.assertEqual(thumb_after_delete.status_code, 404)


if __name__ == '__main__':
    # Run tests with verbosity
    unittest.main(verbosity=2)
