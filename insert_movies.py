from sqlalchemy.orm import Session
from db import SessionLocal
from models import Movie, Rating
import json

def insert_movies_from_json():
    # Open and load your JSON data
    with open("movies.json") as f:
        data = json.load(f)
    
    # Create a session
    session = SessionLocal()

    for movie_data in data["movies"]:
        movie = Movie(
            title=movie_data["Title"],
            year=movie_data["Year"],
            rated=movie_data["Rated"],
            released=movie_data["Released"],
            runtime=movie_data["Runtime"],
            genre=movie_data["Genre"],
            director=movie_data["Director"],
            writer=movie_data["Writer"],
            actors=movie_data["Actors"],
            plot=movie_data["Plot"],
            language=movie_data["Language"],
            country=movie_data["Country"],
            awards=movie_data["Awards"],
            poster=movie_data["Poster"],
            metascore=movie_data["Metascore"],
            imdb_rating=movie_data["imdbRating"],
            imdb_votes=movie_data["imdbVotes"],
            imdb_id=movie_data["imdbID"],
            type=movie_data["Type"],
            dvd=movie_data.get("DVD", None),
            box_office=movie_data.get("BoxOffice", None),
            production=movie_data.get("Production", None),
            website=movie_data.get("Website", None),
            response=movie_data["Response"]
        )
        
        # Insert ratings
        for rating_data in movie_data["Ratings"]:
            rating = Rating(
                source=rating_data["Source"],
                value=rating_data["Value"],
                movie=movie
            )
            session.add(rating)
        
        session.add(movie)

    # Commit the changes
    session.commit()
    session.close()

# Call the function to insert data
insert_movies_from_json()
