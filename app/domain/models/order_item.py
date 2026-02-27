from sqlalchemy import Column, Integer, Numeric, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class OrderItem(Base):
    __tablename__="order_items"
    
    id=Column(Integer, primary_key=True, index=True)
    order_id=Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    variant_id=Column(Integer, ForeignKey("variants.id"), index=True, nullable=False)
    quantity=Column(Integer, nullable=False)
    
    unit_price=Column(Numeric(10, 2), nullable=False)
    order=relationship("Order", back_populates="items")
    variant=relationship("Variant")
    
    @property
    def subtotal(self) -> float:
        """Calcula el subtotal histórico de esta línea."""
        return float(self.quantity * self.unit_price)

    def __repr__(self):
        return f"<OrderItem Variant:{self.variant_id} Qty:{self.quantity} Price:{self.unit_price}>"