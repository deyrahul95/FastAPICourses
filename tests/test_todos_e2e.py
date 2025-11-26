import requests
from http import HTTPStatus

base_url: str = "http://127.0.0.1:8000/api/todos"


def test_get_todos():
    response = requests.get(base_url)
    todos = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(todos) > 0

    for todo in todos:
        check_single_todo(todo=todo, todo_id=todo["id"])


def test_get_todo():
    todo_id: int = 2
    response = requests.get(f"{base_url}/{todo_id}")
    todo = response.json()

    assert response.status_code == HTTPStatus.OK
    check_single_todo(todo_id, todo)


def test_get_todo_404():
    response = requests.get(f"{base_url}/2456789")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_todo():
    input = {"name": "Test 2", "description": "Test for two", "priority": 2}

    response = requests.post(url=base_url, json=input)
    todo = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert todo["id"] > 0
    check_single_todo(todo=todo, todo_id=todo["id"])
    assert todo["name"] == input["name"]
    assert todo["description"] == input["description"]
    assert todo["priority"] == input["priority"]


def test_update_todo():
    todo_id: int = 2
    input = {"description": "Test for two"}

    res = requests.get(url=f"{base_url}/{todo_id}")
    todo = res.json()

    response = requests.put(url=f"{base_url}/{todo_id}", json=input)
    updated_todo = response.json()

    assert response.status_code == HTTPStatus.OK
    assert updated_todo["id"] == todo_id
    check_single_todo(todo=updated_todo, todo_id=todo_id)
    assert updated_todo["name"] == todo["name"]
    assert updated_todo["description"] == input["description"]
    assert updated_todo["priority"] == todo["priority"]


def test_delete_todo():
    todo_id: int = 2

    response = requests.delete(f"{base_url}/{todo_id}")

    assert response.status_code == HTTPStatus.NO_CONTENT


def check_single_todo(todo_id, todo):
    assert isinstance(todo["id"], int)
    assert todo["id"] > 0
    assert todo["id"] == todo_id
    assert todo["description"] is not None
    assert todo["priority"] is not None
    assert isinstance(todo["priority"], int)
    assert todo["priority"] in {1, 2, 3}
