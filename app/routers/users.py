from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.User:
    """Creates a new user account.

    This endppoint receives the user's email and password, validates them, checks if an account already exists,
    and if not, creates a new user in the database.

    :param user: The user creation data from the request body
    :param db: The database session dependency, injected by FastAPI
    :raises HTTPException: If a user with the same email address already exists (status code 400)
    :return: The newly created user object, conforming to the "schemas.User' model, which safely excludes
            the password hash
    """

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)