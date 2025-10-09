from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List
from decimal import Decimal

class CartItemBase(SQLModel):
    quantity:int=Field(default=1, ge=1, description="Cantidad de productos en el carrito")
    
    
class CartItem(CartItemBase, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    subtotal:Optional[Decimal]=Field(default=0)
    
    cart_id:int=Field(foreign_key="cart.id")
    cart:Optional["Cart"]=Relationship(back_populates="items")
    
    
    
    product_id:int=Field(foreign_key="product.id")
    product:Optional["Product"]=Relationship(back_populates="cart_items")#Relacion inversa hacia producto
    
    
    
class CartItemCreate(CartItemBase):
    cart_id:int
    product_id:int
    
class CartItemRead(CartItemBase):
    id:int
    cart_id:int
    product_id:int
    subtotal:Decimal
    
class CartItemUpdate(SQLModel):
    subtotal:Optional[Decimal]=None
    quantity:Optional[int]=None
     