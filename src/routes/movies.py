from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from src.database import MovieModel, get_db
from src.schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema


router = APIRouter()


def format_revenue(movies):
    for movie in movies:
        if isinstance(movie.revenue, float):
            movie.revenue = int(movie.revenue)


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        total_items = await db.execute(select(func.count(MovieModel.id)))
        total_items = total_items.scalar()

        query = select(MovieModel).offset((page - 1) * per_page).limit(per_page)
        result = await db.execute(query)
        movies = result.scalars().all()

    format_revenue(movies)

    total_pages = (total_items + per_page - 1) // per_page
    base_url = f"/movies/?page={page}&per_page={per_page}"
    prev_page = f"{base_url}&page={page - 1}" if page > 1 else None
    next_page = f"{base_url}&page={page + 1}" if page < total_pages else None

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_details(movie_id: int, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(MovieModel).filter(MovieModel.id == movie_id))
        movie = result.scalars().first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    if isinstance(movie.revenue, float):
        movie.revenue = int(movie.revenue)

    return movie
