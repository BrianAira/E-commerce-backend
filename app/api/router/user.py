from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from sqlmodel import Session
from  app.infrastructure.databases.database import get_session

from app.domain.models.user import UserCreate, UserRead, AdminUpdate
from app.infrastructure.security.dependencies import get_current_user
from app.infrastructure.repositories.user import UserRepository
from app.domain.services.user import UserService


router = APIRouter(prefix="/users", tags=["users"])



def get_user_service(session: Session = Depends(get_session)):
    repo = UserRepository(session)
    return UserService(repo, session)


#Traer el perfil del usuario autenticado
@router.get("/me", response_model=UserRead)
def get_my_profile(
    current_user=Depends(get_current_user),
):
    return current_user;

@router.get("/me", response_model=UserRead)
def update_my_profile(
    update_data:AdminUpdate,
    current_user=Depends(get_current_user),
    service:UserService=Depends(get_user_service)
):
    updated=service.update_user(current_user.id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
    current_user=Depends(get_current_user),
    service:UserService=Depends(get_user_service),
):
    ok=service.delete_user(current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")



# @router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
# def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
#     try:
#         # Simulamos que ya recibiste un password hasheado (puede ser en middleware)
#         hashed_password = "hashed_" + user.password
#         return service.register_user(user, hashed_password)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @router.get("/{user_id}", response_model=UserRead)
# def get_user(user_id: int, service: UserService = Depends(get_user_service)):
#     user = service.get_user(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# @router.get("/", response_model=List[UserRead])
# def list_users(service: UserService = Depends(get_user_service)):
#     return service.list_users()


# @router.put("/{user_id}", response_model=UserRead)
# def update_user(
#     user_id: int,
#     update_data: AdminUpdate,
#     service: UserService = Depends(get_user_service)
# ):
#     user = service.update_user(user_id, update_data)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
#     ok = service.delete_user(user_id)
#     if not ok:
#         raise HTTPException(status_code=404, detail="User not found")
