import pytest
from fastapi.testclient import TestClient
from app.main import create_app


# Integration Test: ทดสอบ Router + Dependency + Service + Repository ทำงานร่วมกันจริง
@pytest.fixture
def client():
    return TestClient(create_app())  # สร้างแอปใหม่ = ได้ข้อมูลตั้งต้นใหม่ทุกเทสต์


@pytest.fixture
def token(client):
    credentials = {"username": "admin", "password": "admin123"}
    res = client.post("/api/auth/login", json=credentials)
    return res.json()["token"]


@pytest.fixture
def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_health_returns_200(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_login_wrong_password_returns_401(client):
    credentials = {"username": "admin", "password": "wrong"}
    res = client.post("/api/auth/login", json=credentials)
    assert res.status_code == 401


def test_create_product_without_token_returns_401(client):
    data = {"name": "Monitor", "price": 5990, "stock": 3}
    res = client.post("/api/products", json=data)
    assert res.status_code == 401


def test_create_product_invalid_data_returns_400(client, auth):
    data = {"name": "", "price": -10, "stock": 1}
    res = client.post("/api/products", headers=auth, json=data)
    assert res.status_code == 400
    assert "name is required" in res.json()["details"]
    assert "price must be a number greater than 0" in res.json()["details"]


def test_crud_flow(client, auth):
    # 1) Create
    created = client.post(
        "/api/products",
        headers=auth,
        json={"name": "Monitor", "price": 5990, "stock": 3, "discountPercent": 15},
    )
    assert created.status_code == 201
    assert created.json()["finalPrice"] == 5091.5
    product_id = created.json()["id"]

    # 2) Read
    fetched = client.get(f"/api/products/{product_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Monitor"

    # 3) Update
    updated = client.put(
        f"/api/products/{product_id}",
        headers=auth,
        json={"stock": 10, "discountPercent": 0},
    )
    assert updated.status_code == 200
    assert updated.json()["stock"] == 10
    assert updated.json()["finalPrice"] == 5990

    # 4) Delete
    deleted = client.delete(f"/api/products/{product_id}", headers=auth)
    assert deleted.status_code == 204

    # 5) Verify deleted
    assert client.get(f"/api/products/{product_id}").status_code == 404
