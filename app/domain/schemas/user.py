
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, validator
from sqlmodel import SQLModel

from app.domain.schemas.directions import DirectionResponse


class UserCreate(BaseModel):
    username: str=Field(..., min_length=3, max_length=50)
    email:EmailStr
    password:str=Field(..., min_length=8)
    role:str="client"
    
    @field_validator("role")
    @classmethod
    def role_must_be_valid(cls,v):
        allowed_roles={"client", "admin"}
        if v not in allowed_roles:
            raise ValueError(f"El rol debe ser uno de: {', '.join(sorted(allowed_roles))}.")
        return v 
    
    @field_validator("password")
    @classmethod
    def password_not_hashed(cls,v):
        if v.startswith("$2b$") or v.startswith("$2a$"):
            raise ValueError("La contraseña no debe estar cifrada.")
        return v
    
class UserRead(BaseModel):
    id:int
    username:str
    email:EmailStr
    role:str
    directions:List[DirectionResponse]=[]
    model_config=ConfigDict(from_attributes=True)
        
        
class UserUpdate(BaseModel):
    #Esquema para actualizacion parcial PATCH
    username:Optional[str]=None
    email:Optional[EmailStr]=None
    password:Optional[str]=None
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class UserRegisterResponse(BaseModel):
    user:UserRead
    access_token:str
    token_type:str
    
class Token(BaseModel):
    #Esquema de salida para el token jwt
    access_token:str
    token_type:str="bearer"
    # username:Optional[str]=None
    # id:Optional[int]=None
    # role:Optional[str]=None
    # email:Optional[str]=None
    
    # username:str=Field(..., description="El nombre del usuario autenticado")
    # id:int=Field(..., description="El id del usuario autenticado")
    # role:str=Field(..., description="el rol de usuario autenticado")
    # email:EmailStr=Field(..., description="El email del usuario autenticado")
    
class TokenData(SQLModel):
    id:Optional[int]=None