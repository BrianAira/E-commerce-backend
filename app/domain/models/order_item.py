from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from decimal import Decimal

class OrderItemBase(SQLModel):
    quantity:int=Field(default=1)
    unit_price:Optional[Decimal]=None
    subtotal:Decimal=Field(default=0)
    
class OrderItem(OrderItemBase, table=True):
    id:int=Field(default=None, primary_key=True, unique=True)
    
    order_id:int=Field(foreign_key="order.id")
    product_id: int=Field(foreign_key="product.id")
    
    order:Optional["Order"]=Relationship(back_populates="items")
    product:Optional["Product"]=Relationship()

class OrderItemCreate(OrderItemBase):
    order_id:int
    product_id:int
    pass

class OrderItemRead(OrderItemBase):
    order_id:int
    product_id:int
    pass

class OrderItemUpdate(SQLModel):
    quantity:Optional[int]=None
    subtotal:Optional[Decimal]=None
    unit_price:Optional[Decimal]=None