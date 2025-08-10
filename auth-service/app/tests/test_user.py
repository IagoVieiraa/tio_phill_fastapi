from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user_returns_201():
    response = client.post("/auth/users/create", json={"email": "teste8@exemplo.com", "password": "123456"})
    print(response.json())
    assert response.status_code == 201
    assert "id" in response.json()

def test_create_user_when_email_already_exists_returns_400():
    response = client.post("/auth/users/create", json={"email": "teste8@exemplo.com", "password": "123456"})
    assert response.status_code == 400
    assert "Email already exists" in response.json()["body"]