
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name:str=Field(..., min_length=3, max_length=100)
    description:str=Field(..., max_length=255)
    #Slug para url amigable ej: remeras-oversize
    slug:str=Field(..., min_length=3, max_length=120)
    
class CategoryCreate(CategoryBase):
    # parent_id:Optional[int]=None
    pass
    
class CategoryUpdate(BaseModel):
    name:Optional[str]=None
    description:Optional[str]=None
    slug:Optional[str]=None
    is_active:Optional[bool]=None
    
class CategoryResponse(CategoryBase):
    id:int
    is_active:bool=True
    
    model_config=ConfigDict(from_attributes=True)