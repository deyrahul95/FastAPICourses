from typing import List, Optional

from http import HTTPStatus
from fastapi import FastAPI, HTTPException

from data.todos import todos
from models.todo import Todo, TodoCreate, TodoUpdate


app = FastAPI()


@app.get("/api/todos", status_code=HTTPStatus.OK, response_model=List[Todo])
def get_todos(limit: Optional[int] = None) -> List[Todo]:
    """Get all todos from the DB. Optionally pass limit to get only first few todos"""

    if limit:
        return todos[:limit]

    return todos


@app.get("/api/todos/{todo_id}", status_code=HTTPStatus.OK, response_model=Todo)
def get_todo(todo_id: int) -> Todo:
    """Get todo by it's id"""

    for todo in todos:
        if todo.id == todo_id:
            return todo

    raise HTTPException(
        status_code=404, detail="The requested Todo is not found in the database!"
    )


@app.post("/api/todos", status_code=HTTPStatus.CREATED, response_model=Todo)
def create_todo(request: TodoCreate) -> Todo:
    """Create todo and save it into db"""

    new_todo_id: int = max(todo.id for todo in todos) + 1

    new_todo = Todo(
        id=new_todo_id,
        name=request.name,
        description=request.description,
        priority=request.priority,
    )

    todos.append(new_todo)
    return new_todo


@app.put("/api/todos/{todo_id}", status_code=HTTPStatus.OK, response_model=Todo)
def update_todo(todo_id: int, request: TodoUpdate) -> Todo:
    """Update todo by it's id and save it into db"""

    for todo in todos:
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

    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return

    raise HTTPException(
        status_code=404, detail="The requested Todo is not found in the database!"
    )
