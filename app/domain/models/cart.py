from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal


class CartBase(SQLModel):
    pass


class Cart(CartBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    total_amount:Optional[Decimal]=Field(default=0)
    

    # Relación 1 a 1 con User
    user_id: int = Field(foreign_key="user.id", unique=True, index=True)

    # Relación inversa hacia User
    user: Optional["User"] = Relationship(back_populates="cart")

    # Relación con productos (1 carrito puede tener varios productos)
    items: List["CartItem"] = Relationship(back_populates="cart")


# ---------- MODELOS Pydantic ----------

class CartCreate(SQLModel):
    user_id: int


class CartRead(SQLModel):
    id: int
    user_id: int
    total_amount:Optional[Decimal]


class CartUpdate(SQLModel):
    total_amount:Optional[Decimal]=None
    user_id: Optional[int] = None
    total_amount:Optional[Decimal]
