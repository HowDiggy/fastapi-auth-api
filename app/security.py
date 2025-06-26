from passlib.context import CryptContext

# create a cryptContext instance
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# function to hash a password. hashes a plain-text password using bcrypt
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# fucntion to verify a password. Verifies a plain-text password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

