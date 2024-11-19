from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    authjwt_secret_key: str = ""
    authjwt_access_token_expires: int = 3600  # 1 hour

    class Config:
        env_file = ".env" 