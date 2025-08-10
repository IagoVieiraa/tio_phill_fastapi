from fastapi.testclient import TestClient
from app.main import app
import random

client = TestClient(app)

NUMBER_RANDOM = random.randint(0, 2025)
EMAIL_RANDOM = f"teste{NUMBER_RANDOM}@exemplo.com"

def test_create_user_returns_201():
    response = client.post("/auth/users/create", json={"email": EMAIL_RANDOM, "password": "123456"})
    assert response.status_code == 201
    assert "id" in response.json()

def test_create_user_when_email_already_exists_returns_400():
    response = client.post("/auth/users/create", json={"email": EMAIL_RANDOM, "password": "123456"})
    assert response.status_code == 400
    assert "Email already exists" in response.json()["body"]

def test_create_users_return_400_when_email_or_password_is_null():
    response = client.post("/auth/users/create", json={"email": None, "password":"123456"})
    body = response.json()["body"]
    print(body)
    assert response.status_code == 400
    assert "Email" in body and "invalid" in body