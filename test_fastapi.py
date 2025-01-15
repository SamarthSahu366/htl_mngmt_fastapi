import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db import Base
from models import Room, User
from db import SessionLocal,engine

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture
def test_db():
    db = SessionLocal()
    Base.metadata.create_all(bind=engine)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def create_admin_user(test_db):
    admin_user = User(email="admin@test.com", password="password", is_admin=True)
    test_db.add(admin_user)
    test_db.commit()
    return admin_user

@pytest.fixture
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

def test_add_room(test_db, auth_headers):
    response = client.post(
        "/addroom",
        json={"roomid": 1, "location": "Test Location", "price": 100, "status": "available"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Room added successfully"

def test_delete_room(test_db, auth_headers):
    test_db.add(Room(roomid=1, location="Test Location", price=100, status="available"))
    test_db.commit()
    response = client.delete(
        "/deleteroom",
        json={"roomid": 1},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Room deleted successfully"

def test_update_room(test_db, auth_headers):
    test_db.add(Room(roomid=1, location="Old Location", price=100, status="available"))
    test_db.commit()
    response = client.put(
        "/updateroom",
        json={"roomid": 1, "location": "New Location", "price": 150, "status": "occupied"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Room updated successfully"
    assert response.json()["room"]["location"] == "New Location"
    assert response.json()["room"]["price"] == 150
    assert response.json()["room"]["status"] == "occupied"
