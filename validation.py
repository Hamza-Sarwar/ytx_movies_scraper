from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Movie(BaseModel):
    title: Optional[str] = None
    year: Optional[str] = None
    genre: Optional[str] = None
    rating: Optional[str] = None
    link: Optional[str] = None
