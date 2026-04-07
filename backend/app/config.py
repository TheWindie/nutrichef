from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://nutrichef:nutrichef@db:5432/nutrichef"
    APP_ENV: str = "production"

    class Config:
        env_file = ".env"

settings = Settings()
