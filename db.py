from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base  # Import Base from base.py
from models import Movie, Rating

# Define your database URL
URL_DB = 'postgresql://postgres:ss%407861@localhost:5432/blog_database'

# Create engine and session
engine = create_engine(URL_DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)  # Make sure this is after the engine is created
