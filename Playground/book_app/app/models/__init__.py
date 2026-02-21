from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Book(BaseModel):
    """Response model representing a book in the system."""

    id: int
    title: str
    author: str
    category: str
    updated_at: datetime = Field(default_factory=datetime.now)


class AddBookDto(BaseModel):
    """Request DTO for creating a new book."""

    title: str = Field(..., description="Book title", min_length=5, max_length=100)
    author: str = Field(..., description="Book author", min_length=2, max_length=50)
    category: str = Field(..., description="Book category", min_length=3, max_length=20)


class UpdateBookDto(BaseModel):
    """Request DTO for updating an existing book. All fields are optional."""

    title: Optional[str] = Field(
        default=None, description="Book title", min_length=5, max_length=100
    )
    author: Optional[str] = Field(
        default=None, description="Book author", min_length=2, max_length=50
    )
    category: Optional[str] = Field(
        default=None, description="Book category", min_length=3, max_length=20
    )
