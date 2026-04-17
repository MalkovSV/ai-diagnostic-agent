from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    input_text: str

class TaskResponse(BaseModel):
    id: int
    input_text: str
    status: str
    result: str | None = None
    error: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
