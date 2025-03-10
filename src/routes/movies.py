from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database import MovieModel, get_db
from src.schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: Session = Depends(get_db),
):
    total_items = db.query(func.count(MovieModel.id)).scalar()
    total_pages = (total_items + per_page - 1) // per_page
    movies = (
        db.query(MovieModel)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    base_url = f"/movies/?page={page}&per_page={per_page}"
    prev_page = f"{base_url}&page={page - 1}" if page > 1 else None
    next_page = f"{base_url}&page={page + 1}" if page < total_pages else None

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_details(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return movie

