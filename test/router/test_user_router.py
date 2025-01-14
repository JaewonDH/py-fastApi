import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid
from app.core.exception.error import ErrorCode, ErrorDetailMessage

client = TestClient(app)


@pytest.fixture
def test_user():
    return {
        "email": "testuser@example.com",
        "name": "Test User",
        "address": "123 Test Street",
        "password": "securepassword",
    }


@pytest.fixture
def updated_user():
    return {
        "email": "updateduser@example.com",
        "name": "Updated User",
        "address": "456 Updated Street",
    }


def test_create_user(test_user):
    response = client.delete("/api/users")
    response = client.post("/api/user", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["name"] == test_user["name"]
    assert data["address"] == test_user["address"]
    assert "id" in data


def test_create_user_with_duplicate_email(test_user):
    client.post("/api/user", json=test_user)
    response = client.post("/api/user", json=test_user)
    assert response.status_code == 400
    data = response.json()
    assert "code" in data
    assert data["code"] == ErrorCode.INVALID_INPUT.value
    assert data["message"] == ErrorDetailMessage.duplicate_email.value


def test_create_user_with_invalid_data():
    invalid_user = {"email": "not-an-email", "name": "", "address": "123 Street"}
    response = client.post("/api/user", json=invalid_user)
    assert response.status_code == 422


def test_get_users():
    response = client.get("/api/users/?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "total_count" in data
    assert "users" in data
    assert isinstance(data["users"], list)


def test_get_users_with_invalid_pagination():
    response = client.get("/api/users/?page=0&page_size=-1")
    assert response.status_code == 422


def test_get_user(test_user):
    test_user["email"] = "test1.@test.com"
    create_response = client.post("/api/user", json=test_user)
    user_id = create_response.json()["id"]

    response = client.get(f"/api/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert uuid.UUID(data["id"]) == uuid.UUID(user_id)
    assert data["email"] == test_user["email"]
    assert data["name"] == test_user["name"]


# def test_get_users_with_filters(test_user):
#     client.post("/api/user", json=test_user)
#     response = client.get(f"/api/users/?email={test_user['email']}")
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data["users"]) == 1
#     assert data["users"][0]["email"] == test_user["email"]


def test_update_user(test_user, updated_user):
    test_user["email"] = "test2.@test.com"
    create_response = client.post("/api/user", json=test_user)
    user_id = create_response.json()["id"]

    updated_user["email"] = "updated_user11.@test.com"
    updated_user["id"] = user_id
    response = client.put("/api/user", json=updated_user)
    assert response.status_code == 200
    data = response.json()
    assert uuid.UUID(data["id"]) == uuid.UUID(user_id)
    assert data["email"] == updated_user["email"]
    assert data["name"] == updated_user["name"]


def test_update_nonexistent_user(updated_user):
    updated_user["id"] = str(uuid.uuid4())
    response = client.put("/api/user", json=updated_user)
    assert response.status_code == 404
    data = response.json()
    assert "code" in data
    assert data["code"] == ErrorCode.RESOURCE_NOT_FOUND.value
    assert data["message"] == ErrorDetailMessage.invalid_user.value


def test_update_user_with_invalid_data(test_user):
    test_user["email"] = "test3.@test.com"
    create_response = client.post("/api/user", json=test_user)
    user_id = create_response.json()["id"]

    invalid_update = {"id": user_id, "email": ""}
    response = client.put("/api/user", json=invalid_update)
    assert response.status_code == 422


def test_delete_user(test_user):
    test_user["email"] = "test4.@test.com"
    create_response = client.post("/api/user", json=test_user)
    user_id = create_response.json()["id"]

    response = client.delete(f"/api/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200

    get_response = client.get(f"/api/user/{user_id}")
    assert get_response.status_code == 404
    data = get_response.json()
    assert data["code"] == ErrorCode.RESOURCE_NOT_FOUND.value
    assert data["message"] == ErrorDetailMessage.invalid_user.value


def test_delete_nonexistent_user():
    response = client.delete(f"/api/user/{str(uuid.uuid4())}")
    assert response.status_code == 404
    data = response.json()
    assert "code" in data
    assert "message" in data
    assert data["code"] == ErrorCode.RESOURCE_NOT_FOUND.value
    assert data["message"] == ErrorDetailMessage.invalid_user.value


def test_delete_already_deleted_user(test_user):
    test_user["email"] = "test5.@test.com"
    create_response = client.post("/api/user", json=test_user)
    user_id = create_response.json()["id"]
    client.delete(f"/api/user/{user_id}")

    response = client.delete(f"/api/user/{user_id}")
    assert response.status_code == 404


def test_large_user_list_pagination():
    response = client.delete("/api/users")
    response = client.get("/api/users/?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] >= 0
    for i in range(50):
        client.post(
            "/api/user",
            json={
                "email": f"user{i}@example.com",
                "name": f"User {i}",
                "address": f"{i} Example Street",
                "password": "securepassword",
            },
        )

    response = client.get("/api/users/?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 10
    assert data["total_count"] >= 50

    response = client.get("/api/users/?page=2&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 5
    assert data["total_count"] >= 50

    # Test for pagination
    response = client.get("/api/users/?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 5  # First page with 5 users
    assert data["total_count"] == 50  # Total users in the database

    response = client.get("/api/users/?page=3&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 5  # Third page with 5 users
    assert data["total_count"] == 50

    # Test for name filtering
    response = client.get("/api/users/?page=1&page_size=10&name=User 1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 10  # Only one user with name 'User 1'
    assert data["users"][0]["name"] == "User 1"

    # Test for partial name filtering
    response = client.get("/api/users/?page=1&page_size=10&name=User")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 10  # The first 10 users with 'User' in their name
    assert all("User" in user["name"] for user in data["users"])


def test_get_users_with_invalid_name_filter():
    # Test filtering by invalid name
    response = client.get("/api/users/?page=1&page_size=10&name=NonexistentUser")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 0  # No users match the name
    assert data["total_count"] == 0  # Total count should be 0


def test_get_users_without_name_filter():
    # Test fetching users without filtering by name
    response = client.get("/api/users/?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 10  # 10 users are returned by default
    assert data["total_count"] >= 10  # Ensure that there are at least 10 users


def test_get_users_with_negative_page_size():
    response = client.get("/api/users/?page=1&page_size=-5")
    assert response.status_code == 422  # Invalid page_size should return 422


def test_get_users_with_invalid_page_number():
    response = client.get("/api/users/?page=-1&page_size=10")
    assert response.status_code == 422  # Invalid page number should return 422
