from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/auth/users/create", json={"email": "teste8@exemplo.com", "password": "123456"})
    print(response.json())
    assert response.status_code == 201
    assert "id" in response.json()