from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.user import User, UserCreate, AdminUpdate


class IUserRepository(ABC):
    """Contrato para el repositorio de Usuarios"""

    @abstractmethod
    def create(self, user: UserCreate, hashed_password: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def update(self, user_id: int, user_data: AdminUpdate) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[User]:
        raise NotImplementedError
