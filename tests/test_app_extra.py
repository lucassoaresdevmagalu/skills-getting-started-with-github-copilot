from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_nonexistent_activity():
    response = client.post("/activities/NonexistentActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    response = client.post("/activities/NonexistentActivity/unregister?email=someone@mergington.edu")
    assert response.status_code == 404

def test_unregister_not_registered():
    # Tenta remover um email que não está inscrito
    response = client.post("/activities/Tennis Club/unregister?email=notregistered@mergington.edu")
    assert response.status_code == 400

def test_signup_and_unregister_multiple():
    activity = "Art Studio"
    emails = [f"multi{i}@mergington.edu" for i in range(3)]
    for email in emails:
        r = client.post(f"/activities/{activity}/signup?email={email}")
        assert r.status_code == 200 or r.status_code == 400
    # Remove todos
    for email in emails:
        r = client.post(f"/activities/{activity}/unregister?email={email}")
        assert r.status_code == 200 or r.status_code == 400

def test_get_activities_structure():
    response = client.get("/activities")
    data = response.json()
    for name, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)
