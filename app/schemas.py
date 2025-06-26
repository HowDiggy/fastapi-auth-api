import uuid
from pydantic import BaseModel, ConfigDict

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