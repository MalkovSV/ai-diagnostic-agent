from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Task(Base):
    """
    Модель задачи в системе AI‑агента.

    Представляет задачу, которую необходимо обработать. Хранится в таблице "tasks".

    Attributes:
        id (int): Уникальный идентификатор задачи (первичный ключ).
        input_text (str): Исходный текст, переданный для обработки.
        status (str): Статус задачи. Возможные значения: "pending", "completed", "failed".
        result (str | None): Результат обработки (если есть).
        error (str | None): Описание ошибки (если возникла).
        created_at (datetime): Время создания задачи.
        updated_at (datetime | None): Время последнего обновления статуса.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    status = Column(String, default="pending")
    result = Column(Text)
    error = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)  # nullable=True