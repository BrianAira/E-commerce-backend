from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from decimal import Decimal
from datetime import datetime, timezone

class OrderBase(SQLModel):
    status:str
    total_amount:Decimal
    shipping_address:str

    
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
    