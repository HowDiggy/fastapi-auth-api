from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .users import get_current_user, oauth2_scheme
from .. import crud, security, schemas, models
from .. database import get_db

router = APIRouter(tags=["Authentication"])


def get_current_user_from_refresh_token(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
) -> models.User:
    """
    Dependency to get the current user from the refresh token.

    Decodes the refresh token, validates it, and fetches the user from the database.
    Raisses an exception if the token is invalid or the user does not exist.

    :param token: The refresh token from the Authorization header.
    :param db: The database dependency.
    :raises HTTPException(status_code=401, detail="Could not validate refresh token.")
    :return: The user model instance.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = security.verify_refresh_token(token)

    if email is None:
        raise credentials_exception

    user = crud.get_user_by_email(db, email=email)

    if user is None:
        raise credentials_exception

    return user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
) -> schemas.Token:
    """
    Provides an access token and refresh token for a user after authenticating them.

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
    refresh_token = security.create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(email: str, db: Session = Depends(get_db)) -> schemas.Msg:
    """
    Password recovery endpoint.

    It finds the user by email, generates a time-limited password reset token, and simulates sending it by printing
    it to the console. For security, it returns a generic message regardless of whether the user was found to prevent
    user enumeration attacks.

    This generates a password reset token and "sends" it to the user.
    When implemented into a real application, this would send an email.

    :param email: The email address of the user requesting the password reset.
    :param db: The database session dependency.
    :return: A generic confirmation message.
    """

    user = crud.get_user_by_email(db, email=email)

    if user:
        password_reset_token = security.create_password_reset_token(email=email)

        # in a real app, you would send this token in an email
        # for this demo, we will simply print to console
        print("--- PASSWORD RESET TOKEN ---")
        print(password_reset_token)
        print("----------------------------")

    # Always return a generic success message to prevent user enumeration
    return {"msg": "If an account with that email exists, a password recovery email has been sent."}

@router.post("/reset-password/")
def reset_password(body: schemas.PasswordReset, db: Session = Depends(get_db)):
    """
    Reset the user's password using a valid reset token.

    This endpoint verifies the provided token. If the token is valid and unexpired, it finds the corresponding user and
    updates their password with the new one provided in the request body.

    :param body: The request body containing the reset token and the new password.
    :param db: The database session dependency.
    :raises HTTPException 400: If the token is invalid or has expired.
    :raises HTTPException 404: If no user is found for a valid token (edge case).
    :return: A generic success message.
    """

    email = security.verify_password_reset_token(token=body.token)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid or expired token",
        )

    user = crud.get_user_by_email(db, email=email)
    if not user:
        # this should be impossible if the token is valid, but is a good safeguard
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    crud.update_user_password(db=db, user=user, new_password=body.new_password)

    return {"msg": "Password updated successfully"}

@router.post("/token/refresh/", response_model=schemas.AccessToken)
def refresh_access_token(
        current_user: models.User = Depends(get_current_user_from_refresh_token),
) -> schemas.Token:
    """
    Refreshes an access token using a valid refresh token.

    The refresh token should be provided as a Bearer token in the Authorization header.

    :param current_user: The user object for the currently authenticated user, injected by the dependency.
    :return: A new access token.
    """

    # generate a new access token
    new_access_token = security.create_access_token(data={"sub": current_user.email})

    # return the new access token along with the original refresh token
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }