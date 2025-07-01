from sqlalchemy.orm import Session
from . import models, schemas, security

# creates a new user in the database
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Creates a new user in the database with a hashed password.

    This function encapsulates the logic for creating a user, ensuring that the password is never stored in plain text.

    Pre-conditions:
        - the 'db' session must be an active, valid database session.
        - the 'user email' must not already exist in the database. A violation of this will cause a database
            IntegrityError to be raised.

    Post-conditions: (on successful execution):
        - a new 'User' record is created and committed to the database
        - the password stored in the database is a secure hash of the input password
        - the function returns the newly created 'User' model instance

    :param db: the SQLAlchemy database session
    :param user: the user data (email and plain-text password) from the Pydantic schema
    :return: the newly created SQLAlchemy user model instance
    :raises: IntegrityError: if the user with the same email already exists in the database
    """

    # hash the password from the incoming data
    hashed_password = security.get_password_hash(user.password)

    # create a new database model instance with the hashed password
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )

    # add the user object to the database session
    db.add(db_user)

    # commit the changes to the database
    db.commit()

    # refresh the instance to ge tthe datat that was just saved ( like new ID)
    db.refresh(db_user)

    return db_user

def get_user_by_email(db: Session, email: str) -> models.User | None:
    """
    Retrieves a single user from the database by its email address.
    :param db: The SQLAlchemy database session
    :param email: The email address of the user to retrieve
    :return: The user model instance if a user with the given email exists, None otherwise
    """
    return db.query(models.User).filter(models.User.email == email).first()

def update_user_email(db: Session, user: models.User, new_email: str) -> models.User:
    """
    Updates a user's email address in the database.

    :param db: The SQLAlchemy database session
    :param user: The existing user model instance to update
    :param new_email: The new email address to set for the user.
    :return: The updated user model instance
    :raises: IntegrityError: If the new email address is already taken by another user.
    """

    user.email = new_email
    db.add(user)
    db.commit()
    db.refresh(user)
    return user