from typing import List

from models.todo import Priority, Todo


todos: List[Todo] = [
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
