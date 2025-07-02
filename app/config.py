from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    """
    ---------- Access Token Settings-------------
    """
    MINUTES_TO_REFRESH: int = 30

    # the secret key for singing JWTs
    SECRET_KEY: str

    # the algorithm to use for JWT signing
    ALGORITHM: str = "HS256"

    # the lifetime of the access token in minutes
    ACCESS_TOKEN_EXPIRE_MINUTES: int = MINUTES_TO_REFRESH


    """
    ------------ Refresh Token Settings---------------
    """

    """
    
    DAYS_TO_REFRESH: int = 7
    HOURS_MULTIPLIER: int = 24
    MINUTES_MULTIPLIER: int = 60
    """

    REFRESH_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # MINUTES_MULTIPLIER * HOURS_MULTIPLIER * DAYS_TO_REFRESH

    model_config = SettingsConfigDict(env_file=".env")


# create a single, reusable instance of the Settings class
# our application will import this 'settings' object
settings = Settings()
