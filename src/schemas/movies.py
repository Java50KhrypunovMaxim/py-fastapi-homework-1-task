from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from typing import ClassVar


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: int
    revenue: int
    country: str

    from_attributes: ClassVar[bool] = True

    class Config:
        from_attributes: ClassVar[bool] = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int

    class Config:
        from_attributes: ClassVar[bool] = True
