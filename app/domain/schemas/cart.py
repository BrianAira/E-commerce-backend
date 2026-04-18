from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# from app.domain.schemas.variant import VariantCartOut,


class CartItemBase(BaseModel):
    variant_id:int
    quantity:int=Field(..., ge=1)
    
class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity:int=Field(..., ge=1)
  
class ProductMinOut(BaseModel):
    id:int
    name:str
    price:float
    sku_base:str
    url:Optional[str]=None
    
    model_config=ConfigDict(from_attributes=True)
      
    
    
class VariantCartOut(BaseModel):
    id:int
    color:str
    talle:str
    sku:str
    product:ProductMinOut
    
    model_config=ConfigDict(from_attributes=True)
      
    
class CartItemResponse(CartItemBase):
    id:int
    cart_id:int
    
    variant:Optional[VariantCartOut]=None
    
    model_config=ConfigDict(from_attributes=True)
       
class CartResponse(BaseModel):
    id:int
    user_id:int
    
    items:List[CartItemResponse]=[]
    
    total_items:int=0
    total_price:float=0.0
    
    model_config=ConfigDict(from_attributes=True)
    
    