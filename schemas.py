from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    completed: bool = False

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    completed: bool | None = None

class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TaskPage(BaseModel):
    items: list[TaskRead]
    skip: int
    limit: int
    total: int
