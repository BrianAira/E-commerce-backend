from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class ProductVariantBase(SQLModel):
    size:str=Field(description="Talle: S, M, L, XL...")
    color:str=Field(description="Color:Azul, rojo...")
    stock:int=Field(default=1, ge=0, description="Cantidad disponible")
    sku:Optional[str]=Field(default=None, index=True)

class ProductVariant(ProductVariantBase, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    product_id:int=Field(foreign_key="product.id")
    
    product:Optional["Product"]=Relationship(back_populates="variants")
    order_items:List["OrderItem"]=Relationship(back_populates="product_variant")
class ProductVariantCreate(ProductVariantBase):
    product_id:int
    
    
class ProductVariantRead(ProductVariantBase):
    id:int
    product_id:int

class ProductVariantUpdate(SQLModel):
    size:Optional[str]=None
    color:Optional[str]=None
    stock:Optional[int]=None
    sku:Optional[str]=None