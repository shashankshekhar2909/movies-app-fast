from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  # Import Base from base.py

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    value = Column(String)
    movie_id = Column(Integer, ForeignKey("movies.id"))

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    year = Column(String)
    rated = Column(String)
    released = Column(String)
    runtime = Column(String)
    genre = Column(String)
    director = Column(String)
    writer = Column(String)
    actors = Column(String)
    plot = Column(String)
    language = Column(String)
    country = Column(String)
    awards = Column(String)
    poster = Column(String)
    metascore = Column(String)
    imdb_rating = Column(String)
    imdb_votes = Column(String)
    imdb_id = Column(String)
    type = Column(String)
    dvd = Column(String, nullable=True)
    box_office = Column(String, nullable=True)
    production = Column(String, nullable=True)
    website = Column(String, nullable=True)
    response = Column(String)
    
    ratings = relationship("Rating", backref="movie")
