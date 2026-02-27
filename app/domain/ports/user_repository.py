from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.models.directions import Directions
from app.domain.models.user import User
from app.domain.schemas.directions import DirectionCreate
from app.domain.schemas.user import UserUpdate
from app.domain.schemas.user import UserCreate


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id:int)->Optional[User]:
        pass
    
    @abstractmethod
    def get_by_email(self, email:str)->Optional[User]:
        pass
    
    @abstractmethod
    def create(self, user_data:UserCreate)->User:
        pass
    
    @abstractmethod
    def update(self, user_id:int, user_data:UserUpdate)->Optional[User]:
        pass
    
    # @abstractmethod 
    # def list_all(self, skip:int=0, limit:int=10)->List[User]:
    #     pass
    
    @abstractmethod
    def add_address(self, user_id:int, address_data:DirectionCreate):
        pass
    
    @abstractmethod
    def get_addresses(self, user_id:int)->List[Directions]:
        pass
    
    @abstractmethod
    def get_address_by_id(self, address_id:int)->Optional[Directions]:
        pass
    