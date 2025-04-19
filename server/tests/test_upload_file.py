import io
import pytest
from flask import Flask
from app.routes.upload_file import upload_bp

@pytest.fixture
def client(tmp_path):
    app = Flask(__name__) 
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = str(tmp_path) 
    app.register_blueprint(upload_bp)

    with app.test_client() as client:
        yield client

def test_upload_csv_success(client):
    csv_content = "name,age\nAlice,30\nBob,25\nCharlie,35"
    data = {
        'file': (io.BytesIO(csv_content.encode('utf-8')), 'test.csv')
    }

    response = client.post('/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == 'File processed'
    assert json_data['file'] == 'test.csv'

def test_upload_no_file(client):
    response = client.post('/upload', data={}, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'No file part'

def test_upload_empty_filename(client):
    data = {
        'file': (io.BytesIO(b''), '')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'No selected file'

def test_upload_invalid_file_type(client):
    data = {
        'file': (io.BytesIO(b'Some data'), 'file.txt')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Invalid file type'
