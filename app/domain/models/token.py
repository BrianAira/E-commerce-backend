from pydantic import BaseModel
from app.domain.models.user import UserRead

class Token(BaseModel):
    user:UserRead
    access_token:str
    token_type:str="bearer"
    
# class TokenData(BaseModel):
#     user_id:int|None=None