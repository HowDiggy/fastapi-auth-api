import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# database URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# sessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative base
Base = declarative_base()

def get_db():
    """A FastAPI dependency that provides a SQLAlchemy database session.

    This function is a generator that creates a new SessionLocal instance for each request, yields it to the path operation function,
    and then ensures the session is properly closed after the request is finished, even if an error occurs.

    :yields: An active SQLAlchemy Session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

