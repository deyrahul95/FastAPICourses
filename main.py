from enum import IntEnum
from typing import List, Optional

from http import HTTPStatus
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel, Field

app = FastAPI()


class Priority(IntEnum):
    Low = 3
    Medium = 2
    High = 1


class TodoBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=512, description="Name of the Todo")
    description: str = Field(..., description="Description of the Todo")
    priority: Priority = Field(default=Priority.Low, description="Priority of the Todo")


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int = Field(..., description="Unique identification of the Todo")


class TodoUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=3, max_length=512, description="Name of the Todo"
    )
    description: Optional[str] = Field(None, description="Description of the Todo")
    priority: Optional[Priority] = Field(None, description="Priority of the Todo")


all_todos: List[Todo] = [
    Todo(
        id=1,
        name="FastAPI CC",
        description="Complete the FastAPI Crash Course",
        priority=Priority.High,
    ),
    Todo(
        id=2,
        name="React CC",
        description="Complete the React Crash Course",
        priority=Priority.Medium,
    ),
    Todo(
        id=3,
        name="System Design",
        description="Complete the System Design with C# Course",
        priority=Priority.Medium,
    ),
    Todo(
        id=4,
        name="Clean Architecture",
        description="Complete the Clean Architecture Book",
        priority=Priority.Low,
    ),
    Todo(
        id=5,
        name="Update Resume",
        description="Update the Resume for Full Stack Developer Role",
        priority=Priority.Low,
    ),
]


@app.get("/api/todos", status_code=HTTPStatus.OK, response_model=List[Todo])
def get_todos(limit: Optional[int] = None) -> List[Todo]:
    """Get all todos from the DB. Optionally pass limit to get only first few todos"""

    if limit:
        return all_todos[:limit]

    return all_todos


@app.get("/api/todos/{todo_id}", status_code=HTTPStatus.OK, response_model=Todo)
def get_todo(todo_id: int) -> Todo:
    """Get todo by it's id"""

    for todo in all_todos:
        if todo.id == todo_id:
            return todo

    raise HTTPException(
        status_code=404, detail="The requested Todo is not found in the database!"
    )


@app.post("/api/todos", status_code=HTTPStatus.CREATED, response_model=Todo)
def create_todo(request: TodoCreate) -> Todo:
    """Create todo and save it into db"""

    new_todo_id: int = max(todo.id for todo in all_todos) + 1

    new_todo = Todo(
        id=new_todo_id,
        name=request.name,
        description=request.description,
        priority=request.priority,
    )

    all_todos.append(new_todo)
    return new_todo


@app.put("/api/todos/{todo_id}", status_code=HTTPStatus.OK, response_model=Todo)
def update_todo(todo_id: int, request: TodoUpdate) -> Todo:
    """Update todo by it's id and save it into db"""

    for todo in all_todos:
        if todo.id == todo_id:
            todo.name = request.name if request.name is not None else todo.name
            todo.description = (
                request.description
                if request.description is not None
                else todo.description
            )
            todo.priority = (
                request.priority if request.priority is not None else todo.priority
            )
            return todo

    raise HTTPException(
        status_code=404, detail="The requested Todo is not found in the database!"
    )


@app.delete("/api/todos/{todo_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_todo(todo_id: int) -> None:
    """Delete a todo by it's id"""

    for index, todo in enumerate(all_todos):
        if todo.id == todo_id:
            all_todos.pop(index)
            return

    raise HTTPException(
        status_code=404, detail="The requested Todo is not found in the database!"
    )
