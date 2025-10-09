from jose import JWSError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.domain.models.user import User
from app.domain.models.enum import UserRol
from app.core.config import settings
from sqlmodel import Session, select
from app.infrastructure.databases.database import get_session

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token:str=Depends(oauth2_scheme),
    session:Session=Depends(get_session)
)->User:
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload=jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id:str=payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWSError:
        raise credentials_exception
    user=session.exec(select(User).where(User.id==int(user_id))).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(current_user:User=Depends(get_current_user))->User:
    if current_user.role != UserRol.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene acceso de administrador"
        )
    return current_user