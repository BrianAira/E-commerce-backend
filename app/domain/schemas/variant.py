
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class VariantBase(BaseModel):
    color:str=Field(..., min_length=3, max_length=50)
    talle:str=Field(..., min_length=1, max_length=20)
    sku:str=Field(..., min_length=4, max_length=100)
    stock_current:int=Field(default=0, ge=0)
    stock_min:int=Field(default=5, ge=0)
    
class VariantCreate(VariantBase):
    product_id:Optional[int]=None

class VariantUpdate(BaseModel):
    color:Optional[str]=None
    talle:Optional[str]=None
    stock_current:Optional[int]=None
    stock_min:Optional[int]=None
    
    sku:Optional[str]=None
    
class VariantResponse(VariantBase):
    id:int
    product_id:int
    
    stock_status:Optional[str]=None
    
    model_config=ConfigDict(from_attributes=True)
    