from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, auth

# this command tells SQLAlchemy to create all the tables defined in our models
# it will create 'users' table based on app/models.py file
models.Base.metadata.create_all(bind=engine)

# create an instance of the FastAPI class
app = FastAPI()

# include the router from app/routers/users.py
app.include_router(users.router)
app.include_router(auth.router)
