from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from .config import settings

# create a cryptContext instance
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# function to hash a password. hashes a plain-text password using bcrypt
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# fucntion to verify a password. Verifies a plain-text password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """
    Generate a new JWT access token.

    :param data: The data to encode in the token's payload
    :return: The encoded JWT access token as a string
    """

    to_encode = data.copy()

    # calculate the token's expiration time
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # encode the token with the secret key and algorithm from settings
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt

def create_password_reset_token(email: str) -> str:
    """
    Generates a password reset JWT.

    The token has a short expiration time in minutes.

    :param email: The email of the user to reset password for.
    :return: Returns the encoded JWT access token as a string.
    """
    PASSWORD_RESET_EXPIRE_MINUTES = 10

    expire = datetime.now(timezone.utc) + timedelta(minutes=PASSWORD_RESET_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": email}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

def verify_password_reset_token(token: str) -> str | None:
    """
    Verifies the password reset JWT.

    :param token: The password reset token to verify.
    :return: The user's email if the token is valid, None otherwise.
    """

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None