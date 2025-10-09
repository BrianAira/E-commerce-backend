from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.core.config import settings
from typing import Dict, Any

pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_password_hash(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject:str|int, expires_delta:timedelta|None=None)->str:
    now=datetime.now(timezone.utc)
    if expires_delta is None:
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire=now+expires_delta 
    
    payload:Dict[str, any]={
        "sub":str(subject),
        "iat":int(now.timestamp()),
        "exp":int(expire.timestamp())
    }
    
    token=jwt.encode(payload,settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token
