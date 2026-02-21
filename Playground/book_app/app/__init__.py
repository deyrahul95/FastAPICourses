import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routes import router as book_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    logger.info("Starting Book API application")
    yield
    logger.info("Shutting down Book API application")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Book API",
        description="A RESTful API for managing books with CRUD operations",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(book_router)

    return app


app = create_app()
