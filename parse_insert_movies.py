import pandas as pd
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Movie, Rating

def preprocess_and_insert_movies(file_path: str):
    # Load the Excel file
    df = pd.read_excel(file_path)

    # Open a database session
    db: Session = SessionLocal()
    try:
        for _, row in df.iterrows():
            # Map Excel data to current schema
            title = row["Title"]
            year = row.get("Year")
            rated = row.get("Rating")
            released = row.get("Release Date")
            runtime = row.get("Duration (min)")
            genre = row.get("Genre")
            language = row.get("Language")
            country = row.get("Country")
            director = row.get("Director Name")
            writer = row.get("Writer")
            actors = row.get("Lead Actor")  # Assuming lead actor is being used for the "actors" field
            plot = row.get("Plot")
            imdb_rating = row.get("IMDb Score (1-10)")
            imdb_votes = row.get("IMDb Votes")
            imdb_id = row.get("IMDb ID")
            type = row.get("Type")
            box_office = row.get("Gross Revenue")
            production = row.get("Production")
            website = row.get("Website")
            response = row.get("Response")

            ratings = [
                {"Source": "IMDb", "Value": f"{imdb_rating}/10"} if imdb_rating else None,
                {"Source": "Box Office", "Value": f"${box_office}"} if box_office else None,
            ]
            ratings = [r for r in ratings if r]  # Remove None values

            # Check if the movie already exists
            existing_movie = db.query(Movie).filter(Movie.title == title).first()

            if existing_movie:
                # Update existing movie details if necessary
                existing_movie.year = year or existing_movie.year
                existing_movie.rated = rated or existing_movie.rated
                existing_movie.released = released or existing_movie.released
                existing_movie.runtime = runtime or existing_movie.runtime
                existing_movie.genre = genre or existing_movie.genre
                existing_movie.language = language or existing_movie.language
                existing_movie.country = country or existing_movie.country
                existing_movie.director = director or existing_movie.director
                existing_movie.writer = writer or existing_movie.writer
                existing_movie.actors = actors or existing_movie.actors
                existing_movie.plot = plot or existing_movie.plot
                existing_movie.imdb_rating = imdb_rating or existing_movie.imdb_rating
                existing_movie.imdb_votes = imdb_votes or existing_movie.imdb_votes
                existing_movie.imdb_id = imdb_id or existing_movie.imdb_id
                existing_movie.type = type or existing_movie.type
                existing_movie.box_office = box_office or existing_movie.box_office
                existing_movie.production = production or existing_movie.production
                existing_movie.website = website or existing_movie.website
                existing_movie.response = response or existing_movie.response

                # Add new ratings
                for rating in ratings:
                    new_rating = Rating(source=rating["Source"], value=rating["Value"], movie_id=existing_movie.id)
                    db.add(new_rating)
            else:
                # Create a new Movie object
                new_movie = Movie(
                    title=title,
                    year=year,
                    rated=rated,
                    released=released,
                    runtime=runtime,
                    genre=genre,
                    language=language,
                    country=country,
                    director=director,
                    writer=writer,
                    actors=actors,
                    plot=plot,
                    imdb_rating=imdb_rating,
                    imdb_votes=imdb_votes,
                    imdb_id=imdb_id,
                    type=type,
                    box_office=box_office,
                    production=production,
                    website=website,
                    response=response,
                )
                db.add(new_movie)
                print(new_movie)
                db.flush()  # Ensure new_movie.id is available

                # Add ratings for the new movie
                for rating in ratings:
                    new_rating = Rating(source=rating["Source"], value=rating["Value"], movie_id=new_movie.id)
                    db.add(new_rating)

        # Commit the session
        db.commit()
        print("Movies and ratings inserted/updated successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    file_path = "db.xlsx"
    preprocess_and_insert_movies(file_path)
