

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


# class CartStatus(str, Enum):
#     OPEN = "open"
#     CHECKED_OUT = "checked_out"


class Cart(Base):
    
    __tablename__="carts"
    
    id=Column(Integer, index=True, primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    user=relationship("User", back_populates="cart")
    items=relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")    
    # status: CartStatus = Field(default=CartStatus.OPEN)

    @property
    def total_items(self) -> int:
        """Suma rápida de todas las cantidades en el carrito."""
        return sum(item.quantity for item in self.items)

# class CartItem(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     cart_id: int = Field(
#         sa_column=Column(Integer, ForeignKey("cart.id", ondelete="CASCADE")),
#     )
#     product_id: int = Field(
#         sa_column=Column(Integer, ForeignKey("product.id", ondelete="CASCADE")),
#     )
#     quantity: int = Field(default=1)
#     unit_price: float