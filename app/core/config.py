from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME:str="Mi Odisea API"
    DATABASE_HOSTNAME:str=None
    DATABASE_PORT:int=None
    DATABASE_PASSWORD:str=None
    DATABASE_NAME:str=None
    DATABASE_USERNAME:str=None
    
    DATABASE_URL:str 

    SECRET_KEY:str
    ALGORITHM:str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    MP_ACCESS_TOKEN:str
    MP_WEBHOOK_URL:str
         
    model_config=SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
        )
    
settings=Settings()