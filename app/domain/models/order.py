from datetime import datetime
import enum
from typing import List, Optional
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float, Numeric, String
# from sqlmodel import Field, Relationship, SQLModel

from app.core.database import Base


class OrderStatus(str, enum.Enum):
    PENDING= "pending"
    PAID="paid"
    SHIPPED="shipped"
    DELIVERED="delivered"
    # CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__="orders"
    
    id= Column(Integer,index=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    
    status: OrderStatus = Column(default=OrderStatus.PENDING, nullable=False)
    order_date= Column(DateTime,default=datetime.utcnow, nullable=False)
    # total_amount=Column(Float, nullable=False)
    total_amount=Column(Numeric(10,2), nullable=False)
    
    shipping_address_snapshot=Column(String(500), nullable=False)
    tracking_number=Column(String(100), nullable=True)
    # locality=Column(String(50), default="")
    
    user= relationship("User", back_populates="orders")
    items=relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
    def __repr__(self):
        return f"<Order {self.id} - Status: {self.status} - Total: {self.total_amount}>"
    
    
    #Definir relacion de uno a muchos, carga toda la lista de items al llamar order
    # items: List["OrderItem"]=Relationship(back_populates="order")
    
    

# class OrderItem(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     order_id: int = Field(sa_column=Column(Integer, ForeignKey("order.id", ondelete="CASCADE")))
#     #Relacion inversa uno a muchos
#     # order: "Order"=Relationship(back_populates="items")
#     product_id: int
#     name: str
#     quantity: int
#     unit_price: float
#     line_total: float