from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate

def create_task(db: Session, task: TaskCreate):
    """
    Сохраняет новую задачу в базе данных.

    Создаёт экземпляр модели Task на основе входных данных, добавляет его в сессию,
    совершает транзакцию и обновляет объект, чтобы получить сгенерированный ID.

    Args:
        db (Session): Активная сессия базы данных SQLAlchemy.
        task (TaskCreate): Pydantic-модель с данными для создания задачи.

    Returns:
        Task: Объект задачи после сохранения в БД (содержит актуальный ID и временные метки).
    """
    db_task = Task(input_text=task.input_text)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    """
    Находит задачу в базе данных по её ID.

    Выполняет запрос к БД с фильтрацией по полю id и возвращает первую найденную запись.

    Args:
        db (Session): Активная сессия базы данных SQLAlchemy.
        task_id (int): ID искомой задачи.

    Returns:
        Task | None: Объект задачи, если найден, или None, если запись отсутствует.
    """
    return db.query(Task).filter(Task.id == task_id).first()
