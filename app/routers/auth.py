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
) -> schemas.Token:
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
