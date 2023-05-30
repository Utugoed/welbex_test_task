from pydantic import BaseSettings


class Settings(BaseSettings):

    POSTGRES_USER: str = "welbex"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_HOST: str = "postgres_db"
    POSTGRES_PORT: str = "5432"
    TABLE: str = "welbex"

    CELERY_BROKER_URL: str = "redis://redis_db/0"

    BASE_VEHICLES_AMOUNT: int = 20
    LOCATIONS_AMOUNT: int = 33789

    SEARCH_CIRCLE_RADIUS: int = 450
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()