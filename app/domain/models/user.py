from typing import Optional ,List 
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, BaseModel

class UserBase (SQLModel):
    name: str= Field (index=True)
    email: EmailStr = Field(unique= True , index=True)
    phone: str = Field (index=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashedPassword: str = Field()

    # Relación inversa al carrito (1 a 1)
    cart: Optional["Cart"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password:str

class UserRead(UserBase):
    id: int

class AdminUpdate (SQLModel):
    name: Optional[str]=None
    email: Optional[EmailStr]=None
    phone: Optional[str]= None
    password: Optional[str]=None

class LoginData(BaseModel):
    email: EmailStr
    password: str