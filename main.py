from http import HTTPStatus
from fastapi import FastAPI

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK)
def hello() -> dict:
    return {"message": "Hello World"}
