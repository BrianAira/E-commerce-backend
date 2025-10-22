from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from decimal import Decimal
from datetime import datetime, timezone

from app.domain.models.enum import OrderStatus

class OrderBase(SQLModel):
    status:OrderStatus=Field(default=OrderStatus.PENDING)
    total_amount:Decimal=Field(ge=0)
    shipping_address:str
    payment_method:str
    
class Order(OrderBase, table=True):
    id:int=Field(default=None, primary_key=True, unique=True)
    created_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))

    client_id:int=Field(foreign_key="user.id")

    items:List["OrderItem"]=Relationship(back_populates="order")
    
class OrderCreate(OrderBase):
    client_id:int

    pass

class OrderRead(OrderBase):
    id:int
    client_id:int
    pass

class OrderUpdate(SQLModel):
    status:Optional[str]=None
    total_amount:Optional[Decimal]=None
    payment_method:Optional[str]=None
    # shipping_address:Optional[str]=None
    