from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Soccer Team"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()


def test_unregister_participant_removes_email():
    activity_name = "Basketball Team"
    email = "remove-me@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    assert response.status_code == 200
    assert email not in response.json()["participants"]
