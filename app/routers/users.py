from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .. import crud, schemas, models, security
from ..config import settings
from ..database import get_db



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    """
    Dependency to get the current user from a JWT

    Decodes the token, validates the signature, and fetches the user from the DB.
    Raises an exception if the token is invalid or th suer does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenPayload(sub=email)
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_email(db, email=token_data.sub)
    if user is None:
        raise credentials_exception
    return user

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

@router.get("/me/", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Fetches the profile for the currently authenticated user.
    """

    return current_user

@router.put("/me/", response_model=schemas.User)
def update_user_me(
        user_update: schemas.UserUpdate,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db),
) -> models.User:
    """
    Updates the email for the currently authenticated user.

    This endpoint requires the user to provide their current password to authorize the change. It also
    ensures the new email is not already in use by another account.

    :param user_update: The request body containing the new email and the user's current password.
    :param current_user: The user object for the currently authenticated user,
                         injected by the get_current_user dependency.
    :param db: The database session dependency.
    :raises HTTPException 400: If the provided 'current_password' is incorrect.
    :raises HTTPException 400: If the new email is already registered to another user.
    :return: The updated user object.
    """

    # 1. Verify the user's current password
    if not security.verify_password(user_update.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    # 2. Check if the new email is already taken by another user
    existing_user = crud.get_user_by_email(db, email=user_update.email)
    if existing_user and existing_user.id != current_user.id:
        raise HTTPException(status_code=400, detail="Email already registered by another user")

    # 3. Call the CRUD function to update the email
    return crud.update_user_email(db=db, user=current_user, new_email=user_update.email)