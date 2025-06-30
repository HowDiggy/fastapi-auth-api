from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # the secret key for singing JWTs
    SECRET_KEY: str

    # the algorithm to use for JWT signing
    ALGORITHM: str = "HS256"

    # the lifetime of the access token in minutes
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env")


# create a single, reusable instance of the Settings class
# our application will import this 'settings' object
settings = Settings()
