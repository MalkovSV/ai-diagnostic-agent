from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud, database

# Создаём все таблицы при старте приложения
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="AI Agent Backend",
    version="1.0.0"
    )

def get_db():
    """
    Генератор для получения сессии базы данных.

    Создаёт сессию БД через SessionLocal, отдаёт её в качестве зависимости
    и гарантирует закрытие сессии после завершения работы с ней.

    Yields:
        Session: Сессия базы данных SQLAlchemy.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    """
    Корневой эндпоинт API.

    Возвращает приветственное сообщение и ссылку на документацию.

    Returns:
        dict: Словарь с сообщением и ссылкой на документацию API.
    """
    return {
        "message": "AI Agent Backend API",
        "documentation": "/docs"        
    }

@app.post("/tasks", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Создаёт новую задачу в системе.

    Принимает данные задачи, передаёт их в функцию CRUD для сохранения в БД
    и возвращает объект созданной задачи.

    Args:
        task (schemas.TaskCreate): Данные для создания задачи (Pydantic модель).
        db (Session): Сессия базы данных, внедряемая через Depends.

    Returns:
        schemas.TaskResponse: Объект созданной задачи (Pydantic модель с полями id, input_text и т.д.).
    """
    return crud.create_task(db=db, task=task)

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Получает задачу по её уникальному идентификатору.

    Выполняет поиск задачи в БД. Если задача не найдена, возвращает ошибку 404.

    Args:
        task_id (int): Уникальный идентификатор задачи.
        db (Session): Сессия базы данных, внедряемая через Depends.

    Returns:
        schemas.TaskResponse: Объект найденной задачи.

    Raises:
        HTTPException: Если задача с указанным ID не найдена (статус 404).
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
