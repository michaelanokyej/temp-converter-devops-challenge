import pytest
# from src.app import app
import sys
import os

# Add /app/src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_valid_conversion_correct(client):
    response = client.post("/convert", json={
        "value": 84.2,
        "from_unit": "fahrenheit",
        "to_unit": "rankine",
        "student_response": 543.9
    })
    assert response.json["output"] == "correct"

def test_valid_conversion_incorrect(client):
    response = client.post("/convert", json={
        "value": 317.33,
        "from_unit": "kelvin",
        "to_unit": "fahrenheit",
        "student_response": 111.56
    })
    assert response.json["output"] == "incorrect"

def test_invalid_conversion(client):
    response = client.post("/convert", json={
        "value": 136.1,
        "from_unit": "dogcow",
        "to_unit": "celsius",
        "student_response": 45.32
    })
    assert response.json["output"] == "invalid"
