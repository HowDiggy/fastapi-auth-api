from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# database URL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://user:password@db:5432/fastapi_auth_db"

# SQLAlchemy Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# sessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative base
Base = declarative_base()