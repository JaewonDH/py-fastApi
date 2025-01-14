import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid
from app.core.exception.error import ErrorCode, ErrorDetailMessage
import logging

client = TestClient(app)

logger = logging.getLogger("test")


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
    response = client.post("/api/user", json=test_user)
    assert response.status_code == 200
    user_data = response.json()

    response = client.post(
        "/api/post",
        json={"title": "Test1", "content": "content1", "user_id": user_data["id"]},
    )

    assert response.status_code == 200
    post_data = response.json()

    logger.info(f"post_data={post_data}")

    response = client.post(
        "/api/comment",
        json={
            "title": "comment1",
            "content": "comment1",
            "post_id": post_data["id"],
            "user_id": user_data["id"],
        },
    )
    comment_data_1 = response.json()

    response = client.post(
        "/api/comment",
        json={
            "title": "comment2",
            "content": "comment2",
            "post_id": post_data["id"],
            "user_id": user_data["id"],
        },
    )
    comment_data_2 = response.json()

    response = client.post(
        "/api/comment",
        json={
            "title": "comment3",
            "content": "comment3",
            "post_id": post_data["id"],
            "user_id": user_data["id"],
        },
    )
    comment_data_3 = response.json()

    response = client.post(
        "/api/comment",
        json={
            "title": "comment2-1",
            "content": "comment2-1",
            "post_id": post_data["id"],
            "user_id": user_data["id"],
            "parent_id": comment_data_2["id"],
        },
    )

    response = client.post(
        "/api/comment",
        json={
            "title": "comment2-2",
            "content": "comment2-2",
            "post_id": post_data["id"],
            "user_id": user_data["id"],
            "parent_id": comment_data_2["id"],
        },
    )
