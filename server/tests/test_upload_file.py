import io
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'app/assets'
    with app.test_client() as client:
        yield client

def test_upload_csv(client):
    data = {
        'file': (io.BytesIO(b"name,email\nAlice,alice@example.com\nBob,bob@example.com"), 'test.csv')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert "message" in json_data
    assert json_data["message"] == "File processed"
    assert "data" in json_data
    assert json_data["data"]["rows"] == 2
    assert "name" in json_data["data"]["columns"]
    assert "email" in json_data["data"]["columns"]
