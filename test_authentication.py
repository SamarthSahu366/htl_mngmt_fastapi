import pytest
from fastapi.testclient import TestClient
from main import app
from models import User
from db import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/roomManagement"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = 'nogutsnoglory'
REFRESH_SECRET_KEY = 'NOPAINNNOGAIN'

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def setup_db():
    User.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    hashed_password = pwd_context.hash("testpassword")
    db.add(User(username="testuser", email="testuser@example.com", password=hashed_password))
    db.commit()
    db.close()
    yield
    User.metadata.drop_all(bind=engine)

def generate_test_token(email, key, exp_minutes=15):
    expire = datetime.utcnow() + timedelta(minutes=exp_minutes)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, key, algorithm="HS256")

def test_signin_get():
    response = client.get("/users/signup")
    assert response.status_code == 200
    assert response.text == '"this is a sign up page"'

def test_signup_post(setup_db):
    response = client.post(
        "/users/signup",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword"
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "newuser@example.com"

def test_signup_existing_user(setup_db):
    response = client.post(
        "/users/signup",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_post(setup_db):
    response = client.post(
        "/users/login",
        json={
            "email": "testuser@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_login_invalid_user(setup_db):
    response = client.post(
        "/users/login",
        json={
            "email": "invalid@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User doesn't exist"

def test_login_incorrect_password(setup_db):
    response = client.post(
        "/users/login",
        json={
            "email": "testuser@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 504
    assert response.json()["detail"] == "Incorrect password"

def test_protected_route(setup_db):
    token = generate_test_token("testuser@example.com", SECRET_KEY)
    response = client.post(
        "/users/protected_route",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "testuser@example.com"

def test_protected_route_invalid_token(setup_db):
    response = client.post(
        "/users/protected_route",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Could not validate credentials"
