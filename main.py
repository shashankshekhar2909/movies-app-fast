from fastapi import FastAPI, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Movie, Rating
from sqlalchemy import or_

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/movies/")
def get_movies(
    db: Session = Depends(get_db),
    search: str = Query(None, max_length=100),
    limit: int = Query(10, le=100)  # Default limit is 10, max 100
):
    query = db.query(Movie)

    # Apply search filters if search parameter is provided
    if search:
        query = query.filter(
            or_(
                Movie.title.ilike(f"%{search}%"),
                Movie.director.ilike(f"%{search}%"),
                Movie.genre.ilike(f"%{search}%"),
                Movie.actors.ilike(f"%{search}%")
            )
        )

    # Apply limit after filtering
    query = query.limit(limit)

    movies = query.all()

    if not movies:
        raise HTTPException(status_code=404, detail="Movies not found")
    
    # Fetch associated ratings for each movie
    result = []
    for movie in movies:
        movie_data = movie.__dict__
        movie_data["ratings"] = [{"source": rating.source, "value": rating.value} for rating in movie.ratings]
        result.append(movie_data)
    
    return result
