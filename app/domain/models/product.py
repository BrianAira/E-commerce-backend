# app/domain/models/product.py
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal

class ProductBase(SQLModel):
    name: str
    description: Optional[str] = None
    entry_price: Decimal
    sale_price:Decimal
    is_active:bool=Field(default=True)
    category:str=Field(min_length=2, max_length=100)
    stock: int

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    cart_items:List["CartItem"]=Relationship(back_populates="product")

    # Relación 1 a muchos con Cart: cada producto pertenece a un carrito
    # cart_id: Optional[int] = Field(default=None, foreign_key="cart.id")
    # cart: Optional["Cart"] = Relationship(back_populates="product")


class ProductCreate(ProductBase):
    pass
    # cart_id: Optional[int] = None  # al crear un producto, puede asignarse a un carrito

class ProductRead(ProductBase):
    id: int
    # cart_id: Optional[int] = None
  
class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    entry_price: Optional[Decimal] = None
    sale_price:Optional[Decimal]=None
    is_active:Optional[bool]=None
    stock: Optional[int] = None
    category:Optional[str]=None
    # cart_id: Optional[int] = None

class ProductRead(ProductBase):
    id: int
