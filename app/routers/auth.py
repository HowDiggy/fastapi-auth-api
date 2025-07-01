from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud, security, schemas
from .. database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
) -> dict:
    """
    Provides an access token for a user after authenticating them.

    :param form_data: The user's credentials (username and password) sent as form data.
                      FastAPI's OAuth2PasswordRequestForm dependency handles this.
    :param db: The database session dependency.
    :raises HTTPException: If the user is not found or the password is incorrect.
    :return: A dictionary containing the access token and token type.
    """

    user = crud.get_user_by_email(db, email=form_data.username)

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}