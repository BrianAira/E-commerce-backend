from typing import List, Optional
from sqlmodel import Session

from app.domain.models.user import User, UserCreate, UserRead, AdminUpdate
from app.application.ports.user_port import IUserRepository


class UserService:
    def __init__(self, repo: IUserRepository, session: Session):
        self.repo = repo
        self.session = session

    def register_user(self, user_create: UserCreate, hashed_password: str) -> User:
        user = User(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        email=user_create.email,
        phone=user_create.phone,
        address=user_create.address,
        
        hashedPassword=hashed_password  # ya está incluido
    )
        return self.repo.create(user)
      
    def get_user(self, user_id: int) -> Optional[UserRead]:
        user = self.repo.get_by_id(user_id)
        return UserRead.from_orm(user) if user else None

    def update_user(self, user_id: int, update_data: AdminUpdate) -> Optional[UserRead]:
        user = self.repo.update(user_id, update_data)
        return UserRead.from_orm(user) if user else None

    def delete_user(self, user_id: int) -> bool:
        return self.repo.delete(user_id)

    def list_users(self) -> List[UserRead]:
        users = self.repo.list_all()
        return [UserRead.from_orm(u) for u in users]
