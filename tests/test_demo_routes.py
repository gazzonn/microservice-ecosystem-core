from fastapi.testclient import TestClient

from demo_microservice.app.main import app


client = TestClient(app)


def test_public_endpoint_returns_success() -> None:
    response = client.get("/demo/public")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["scope"] == "public"


def test_private_endpoint_requires_user_header() -> None:
    response = client.get("/demo/private")

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing user context"


def test_admin_endpoint_rejects_non_admin_role() -> None:
    response = client.get("/demo/admin", headers={"x-user-id": "user-1", "x-user-roles": "USER"})

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin role required"


def test_admin_endpoint_accepts_admin_role() -> None:
    response = client.get("/demo/admin", headers={"x-user-id": "user-1", "x-user-roles": "ADMIN"})

    assert response.status_code == 200
    assert response.json()["data"]["scope"] == "admin"
