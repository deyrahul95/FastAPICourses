from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str
    updated_at: datetime = datetime.now()


class AddBookDto(BaseModel):
    title: str = Field(..., description="Book title", min_length=5, max_length=100)
    author: str = Field(..., description="Book author", min_length=2, max_length=50)
    category: str = Field(..., description="Book category", min_length=3, max_length=20)


class UpdateBookDto(BaseModel):
    title: Optional[str] = Field(
        default=None, description="Book title", min_length=5, max_length=100
    )
    author: Optional[str] = Field(
        default=None, description="Book author", min_length=2, max_length=50
    )
    category: Optional[str] = Field(
        default=None, description="Book category", min_length=3, max_length=20
    )
