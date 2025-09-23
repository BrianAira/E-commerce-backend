from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class CartBase(SQLModel):
    pass


class Cart(CartBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relación 1 a 1 con User
    user_id: int = Field(foreign_key="user.id", unique=True, index=True)

    # Relación inversa
    user: "User" = Relationship(back_populates="cart")


# ---------- MODELOS Pydantic ----------

class CartCreate(SQLModel):
    user_id: int   # lo único que se necesita para crear un carrito


class CartRead(SQLModel):
    id: int
    user_id: int


class CartUpdate(SQLModel):
    user_id: Optional[int] = None
