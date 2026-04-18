import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """
    Фикстура pytest для настройки БД перед каждым тестом.

    Перед каждым тестом создаёт все таблицы в БД, а после выполнения теста — удаляет их.
    Обеспечивает чистоту окружения для каждого тестового случая.

    Yields:
        None: Ничего не возвращает, только выполняет настройку и очистку.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_task():
    """
    Тест для проверки создания новой задачи.

    Отправляет POST-запрос на /tasks с тестовыми данными и проверяет:
    - статус ответа 200;
    - соответствие input_text отправленному;
    - статус задачи по умолчанию "pending".
    """
    response = client.post("/tasks", json={"input_text": "Test text"})
    assert response.status_code == 200
    data = response.json()
    assert data["input_text"] == "Test text"
    assert data["status"] == "pending"

def test_get_task():
    """
    Тест для проверки получения задачи по ID.

    Последовательность действий:
    1. Создаёт задачу через POST /tasks.
    2. Извлекает ID созданной задачи.
    3. Отправляет GET-запрос на /tasks/{task_id}.
    4. Проверяет:
       - статус ответа 200;
       - совпадение ID;
       - соответствие input_text.
    """
    # Create task first
    create_response = client.post("/tasks", json={"input_text": "Test text"})
    task_id = create_response.json()["id"]

    # Get task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["input_text"] == "Test text"
