from typing import Optional ,List 
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, BaseModel
from app.domain.models.enum import UserRol

class UserBase (SQLModel):
    first_name: str= Field (index=True)
    last_name:str=Field(min_length=2, max_length=20)
    email: EmailStr = Field(unique= True , index=True)
    phone: Optional[str] = Field (index=True, min_length=8, max_length=10)
    address:str=Field(max_length=100, min_length=2, index=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashedPassword: str
    role:Optional[UserRol]=UserRol.CUSTOMER
    # Relación inversa al carrito (1 a 1)
    cart: Optional["Cart"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password:str
    role:UserRol
class UserRead(UserBase):
    id:int
    pass

class AdminUpdate (SQLModel):
    first_name: Optional[str]=None
    last_name:Optional[str]=None
    address:Optional[str]=None
    email: Optional[EmailStr]=None
    phone: Optional[str]= None
    password: Optional[str]=None

class LoginData(BaseModel):
    email: EmailStr
    password: str