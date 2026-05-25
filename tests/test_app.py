from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)

def test_root_redirect():
    # Arrange: Test client is ready
    # Act
    response = client.get("/", follow_redirects=False)
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload

def test_signup_for_activity():
    # Arrange
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]

def test_signup_duplicate_fails():
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_activity_not_found():
    # Arrange
    email = "notfound@mergington.edu"
    activity_name = "Nonexistent"
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_remove_participant():
    # Arrange
    email = "daniel@mergington.edu"
    activity_name = "Chess Club"
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]

def test_remove_participant_not_found():
    # Arrange
    email = "missing@mergington.edu"
    activity_name = "Chess Club"
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"

def test_remove_activity_not_found():
    # Arrange
    email = "anyone@mergington.edu"
    activity_name = "Nonexistent"
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
