from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from decimal import Decimal

class OrderItemBase(SQLModel):
    quantity:int=Field(default=1, ge=1)
    unit_price:Decimal=Field(ge=0, description="Precio unitario al momento de compra")
    subtotal:Decimal=Field(default=0, ge=0)
    
class OrderItem(OrderItemBase, table=True):
    id:int=Field(default=None, primary_key=True, unique=True)
    create_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
    
    order_id:int=Field(foreign_key="order.id")
    product_id: int=Field(foreign_key="product.id")
    product_variant_id:int=Field(foreign_key="productvariant.id")
    
    order:Optional["Order"]=Relationship(back_populates="items")
    product:Optional["Product"]=Relationship()
    product_variant:Optional["ProductVariant"]=Relationship()

class OrderItemCreate(OrderItemBase):
    order_id:int
    product_id:int
    product_variant_id:Optional[int]=None
    # pass

class OrderItemRead(OrderItemBase):
    id:int
    order_id:int
    product_id:int
    product_variant_id:Optional[int]
    create_at:datetime
    # pass

class OrderItemUpdate(SQLModel):
    quantity:Optional[int]=None
    subtotal:Optional[Decimal]=None
    unit_price:Optional[Decimal]=None