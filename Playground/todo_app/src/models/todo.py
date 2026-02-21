from enum import IntEnum
from pydantic import BaseModel, Field
from typing import Optional


class Priority(IntEnum):
    Low = 3
    Medium = 2
    High = 1


class __TodoBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=512, description="Name of the Todo")
    description: str = Field(..., description="Description of the Todo")
    priority: Priority = Field(default=Priority.Low, description="Priority of the Todo")


class TodoCreate(__TodoBase):
    pass


class Todo(__TodoBase):
    id: int = Field(..., description="Unique identification of the Todo")


class TodoUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=3, max_length=512, description="Name of the Todo"
    )
    description: Optional[str] = Field(None, description="Description of the Todo")
    priority: Optional[Priority] = Field(None, description="Priority of the Todo")


__all__ = ["Todo", "TodoCreate", "TodoUpdate", "Priority"]
