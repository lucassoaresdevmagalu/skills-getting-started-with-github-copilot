import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Tennis Club" in data

def test_signup_and_unregister():
    # Signup
    email = "testuser@mergington.edu"
    activity = "Tennis Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200 or response.status_code == 400
    # Try to signup again (should fail)
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    # Unregister
    response3 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response3.status_code == 200
    # Try to unregister again (should fail)
    response4 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response4.status_code == 400

def test_root_redirect():
    response = client.get("/")
    assert response.status_code in (200, 307, 308)
