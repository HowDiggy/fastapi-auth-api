import uuid
from pydantic import BaseModel, ConfigDict, EmailStr

# base schema with shared attributes
class UserBase(BaseModel):
    email: str
    is_active: bool | None = True

# schema for creating a user (expects a password)
class UserCreate(UserBase):
    password: str

# schema for reading/returning user data from the api
class User(UserBase):
    id: uuid.UUID

    # tells Pydantic to read the data even if it is not a dict, but an ORM model
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class TokenPayload(BaseModel):
    sub: str | None = None

class UserUpdate(BaseModel):
    """
    Schema for the user update request body.
    """
    email: EmailStr
    current_password: str

class PasswordReset(BaseModel):
    """
    Schema for the password reset request body.
    """
    token: str
    new_password: str

class Msg(BaseModel):
    """
    Schema for generic messages.
    """
    msg: str

class AccessToken(BaseModel):
    """
    Schema for returning just an access token.
    """
    access_token: str
    token_type: str