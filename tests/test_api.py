import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_task():
    response = client.post("/tasks", json={"input_text": "Test text"})
    assert response.status_code == 200
    data = response.json()
    assert data["input_text"] == "Test text"
    assert data["status"] == "pending"

def test_get_task():
    # Create task first
    create_response = client.post("/tasks", json={"input_text": "Test text"})
    task_id = create_response.json()["id"]

    # Get task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["input_text"] == "Test text"
