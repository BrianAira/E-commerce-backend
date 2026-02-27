from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME:str="Mi Odisea API"
    # DATABASE_URL:str = "mysql+mysqlconnector://user:secret@localhost:3306/final"
    DATABASE_URL:str = "postgresql+psycopg2://myuser:mypassword@localhost:5433/apiBrian"

    SECRET_KEY:str="super_secret_key"
    ALGORITHM:str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
settings=Settings()