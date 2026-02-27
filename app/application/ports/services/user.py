from typing import List, Optional
from app.core.security import get_password_hash, verify_password
from app.domain.models.directions import Directions
from app.domain.models.user import User, UserRole
from app.domain.ports.cart_repository import ICartRepository
from app.domain.ports.user_repository import IUserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, user_repo:IUserRepository, cart_repo:ICartRepository):
        self.user_repo=user_repo
        self.cart_repo=cart_repo
        
    def create_user_as_client(self, user_data:UserCreate)->User:
                
    # def register_user(self, user_data:UserCreate)->User:
        existing_user=self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email ya registrado")
        user_data.role=UserRole.CLIENT
        
        user_data.password=get_password_hash(user_data.password)
        new_user=self.user_repo.create(user_data)
        self.cart_repo.create_cart(user_id=new_user.id)
        
        return new_user
    
    def create_user_as_admin(self, user_data:UserCreate, creator_id:int)->User:
        #Verificar si el creador es un admin existente
        creator=self.user_repo.get_by_id(creator_id)
        if not creator or creator.role != UserRole.ADMIN:
            raise PermissionError("No tienes permisos para crear administradores")
        
        #validar email duplicado
        if self.user_repo.get_by_email(user_data.email):
            raise ValueError("Email ya registrado")
        
        
        user_data.role=UserRole.ADMIN
        user_data.password=get_password_hash(user_data.password)
        
        return self.user_repo.create(user_data)
    
    def get_user_profile(self, user_id:int)->Optional[User]:
        user=self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrad")        
        return user
    
    def add_new_address(self, user_id:int, address_data:dict)->Directions:
        user=self.user_repo.get_by_id(user_id)
        
        if not user:
            raise ValueError("Usuario no encontrado")
        return self.user_repo.add_address(user_id, address_data)
    
    def list_user_address(self, user_id:int)->List[Directions]:
        return self.user_repo.get_addresses(user_id)
    
    def authenticate_user(self, email:str, password:str):
        user=self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user