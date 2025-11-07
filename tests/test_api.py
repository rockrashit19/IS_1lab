import pytest
from app import create_app
from app.database import db
from app.models import User
from passlib.hash import bcrypt
import json

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:" 
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register_and_login_and_get_data(client):
    rv = client.post("/auth/register", json={"username": "alice", "password": "S3cretPass!"})
    assert rv.status_code in (201, 409)

    rv = client.post("/auth/login", json={"username": "alice", "password": "S3cretPass!"})
    assert rv.status_code == 200
    data = rv.get_json()
    assert "access_token" in data
    token = data["access_token"]

    rv = client.get("/api/data", headers={"Authorization": f"Bearer {token}"})
    assert rv.status_code == 200
    data = rv.get_json()
    assert "data" in data
