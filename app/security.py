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