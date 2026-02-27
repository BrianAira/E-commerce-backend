

from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, PrimaryKeyConstraint, UniqueConstraint
from app.core.database import Base
from sqlalchemy.orm import relationship


class CartItem(Base):
    __tablename__="cart_items"
    
    id=Column(Integer, index=True, unique=True, primary_key=True)
    cart_id=Column(Integer, ForeignKey("carts.id"), nullable=False)
    variant_id=Column(Integer, ForeignKey("variants.id"), nullable=False)
    
    quantity=Column(Integer, nullable=False, default=1)
    
    # __table_args__=(
    #     PrimaryKeyConstraint("cart_id", "variant_id"),
        
    # )
    __table_args__ = (
        # Asegura que no se repita la misma variante en el mismo carrito
        UniqueConstraint('cart_id', 'variant_id', name='unique_cart_variant'),
        # Cantidad mínima de 1
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )
    cart= relationship("Cart", back_populates="items")
    variant=relationship("VariantProduct")