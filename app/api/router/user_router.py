from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.application.services.user import UserService
from app.core.database import get_db
from app.core.security import create_access_token, get_current_user
from app.domain.models.user import User
from app.domain.schemas.directions import DirectionCreate, DirectionResponse
from app.infrastructure.repositories.cart import SQLCartRepository
from app.infrastructure.repositories.user import SQLUserRepository
from app.domain.schemas.user import UserCreate, UserRead, Token, UserRegisterResponse


router=APIRouter(prefix="/users", tags=["Users"])
 
def get_user_service(db:Session=Depends(get_db))->UserService:
    return UserService(
        user_repo=SQLUserRepository(db),
        cart_repo=SQLCartRepository(db)
        )
    
@router.post("/register", response_model=UserRegisterResponse)
def register(
    user_data:UserCreate,
    service:UserService=Depends(get_user_service)
):
    try:
        # return service.create_user_as_client(user_data)
        user=service.create_user_as_admin(user_data)
        access_token=create_access_token(data={"sub":str(user.id)})
        return {
            "user":user,
            "access_token":access_token,
            "token_type":"bearer"
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/login", response_model=Token)
def login(
    form_data:OAuth2PasswordRequestForm=Depends(),
    service:UserService=Depends(get_user_service)
):
    user=service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrecta",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token=create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type":"bearer"}


# Rutas protegidas

@router.get("/me", response_model=UserRead)
def get_my_profile(current_user:User=Depends(get_current_user)):
    return current_user

@router.post("/addresses", response_model=DirectionResponse)
def add_address(
    address_data:DirectionCreate,
    current_user:User=Depends(get_current_user),
    service:UserService=Depends(get_user_service)
):
    return service.add_new_address(current_user.id, address_data)

@router.get("/addresses", response_model=List[DirectionResponse])
def get_my_addresses(
    current_user:User=Depends(get_current_user),
    service:UserService=Depends(get_user_service)
):
    return service.list_user_address(current_user.id)

