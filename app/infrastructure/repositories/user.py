from typing import List, Optional
from sqlmodel import Session
from app.domain.models.directions import Directions
from app.domain.models.user import User, UserRole
from app.domain.ports.user_repository import IUserRepository
from app.schemas.user import UserCreate


class SQLUserRepository(IUserRepository):
    def __init__(self, db:Session):
        self.db=db
        
    def get_by_id(self, user_id:int)->Optional[User]:
        return self.db.query(User).filter(User.id==user_id).first()
    
    def get_by_email(self, email:str)->Optional[User]:
        return self.db.query(User).filter(User.email==email).first()
    
    def create(self, user_data:UserCreate)->User:
        new_user=User(
            name=user_data.name,
            email=user_data.email,
            
            password=user_data.password,
            role=user_data.role
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    # def update_role(self, user_id:int, role:UserRole)
    
    def add_address(self, user_id:int, address_data:dict)->Directions:
        new_address=Directions(**address_data, user_id=user_id)
        self.db.add(new_address)
        self.db.commit()
        self.db.refresh(new_address)
        
        return new_address
    
    def get_addresses(self, user_id:int)->List[Directions]:
        return self.db.query(Directions).filter(Directions.user_id==user_id).all()
    