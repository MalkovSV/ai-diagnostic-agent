from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate

def create_task(db: Session, task: TaskCreate):
    db_task = Task(input_text=task.input_text)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()
