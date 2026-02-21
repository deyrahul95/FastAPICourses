import logging
from fastapi import FastAPI
from app.routes import router as book_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Book API",
        description="A simple book management API with CRUD operations",
        version="1.0.0",
    )

    app.include_router(book_router)

    return app


app = create_app()
