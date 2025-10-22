

from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class ProductImageBase(SQLModel):
    url:str
    is_main:bool=Field(default=False)
    alt_text:Optional[str]=None
    
    
class ProductImage(ProductImageBase, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    product_id:int=Field(foreign_key="product.id")
    
    product:Optional["Product"]=Relationship(back_populates="images")
    
class ProductImageCreate(ProductImageBase):
    product_id:int
    
class ProductImageRead(ProductImageBase):
    product_id:int
    id:int
    
class ProductImageUpdate(SQLModel):
    url:Optional[str]=None
    is_main:Optional[bool]=None
    alt_text:Optional[str]=None
    Product_id:Optional[int]=None