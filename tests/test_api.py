from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint returns 200 and expected status."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
