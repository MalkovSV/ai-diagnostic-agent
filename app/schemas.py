from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TaskCreate(BaseModel):
    """
    Схема для создания новой задачи.

    Используется при POST‑запросах к /tasks. Валидирует входные данные.

    Attributes:
        input_text (str): Текст, который нужно обработать. Обязательное поле.
    """
    input_text: str

class TaskResponse(BaseModel):
    """
    Схема ответа с данными задачи.

    Возвращается при успешном создании или получении задачи. Соответствует модели Task.

    Attributes:
        id (int): Уникальный ID задачи.
        input_text (str): Исходный текст.
        status (str): Текущий статус задачи.
        result (str | None): Результат обработки. Может отсутствовать.
        error (str | None): Описание ошибки. Может отсутствовать.
        created_at (datetime): Время создания.
        updated_at (datetime | None): Время последнего обновления. Может быть None.
    """
    id: int
    input_text: str
    status: str
    result: str | None = None
    error: str | None = None
    created_at: datetime
    updated_at: datetime | None = None  # Теперь может быть None

    model_config = ConfigDict(from_attributes=True)
