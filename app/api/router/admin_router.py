

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.security import get_password_hash
from app.domain.models.enum import UserRol
from app.domain.models.user import AdminUpdate, UserCreate, UserRead
from app.infrastructure.databases.database import get_session
from app.infrastructure.security.dependencies import get_current_admin
from app.infrastructure.repositories.user import UserRepository
from app.domain.services.user import UserService


router = APIRouter(prefix="/admin/users", tags=["admin-users"])

def get_user_service(session:Session=Depends(get_session)):
    repo=UserRepository(session)
    return UserService(repo, session)

#Solo admin puede listar usuarios
@router.get("/", response_model=List[UserRead])
def list_users(
    service:UserService=Depends(get_user_service),
    admin=Depends(get_current_admin),
    
):
    return service.list_users()

@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(
    user_id:int, 
    service:UserService=Depends(get_user_service),
    admin=Depends(get_current_admin)
):
    
    user=service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_as_admin(
    user:UserCreate,
    service:UserService=Depends(get_user_service),
    admin=Depends(get_current_admin)
):
    hashed_password=get_password_hash(user.password)
    return service.register_user(user, hashed_password, role=UserRol.ADMIN)

@router.put("/{user_id}", response_model=UserRead)
def update_user_as_admin(
    user_id:int,
    update_data:AdminUpdate,
    service:UserService=Depends(get_user_service),
    admin=Depends(get_current_admin)
):
    user=service.update_user(user_id, update_data)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_as_admin(
    user_id:int,
    service:UserService=Depends(get_user_service),
    admin=Depends(get_current_admin)
):
    ok= service.delete_user(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    