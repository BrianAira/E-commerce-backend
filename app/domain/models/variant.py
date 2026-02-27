
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint, Column, Float, ForeignKey, Integer, String
from app.core.database import Base


class VariantProduct(Base):
    __tablename__="variants"
    
    id=Column(Integer, primary_key=True, index=True)
    
    color=Column(String(50), nullable=False)
    talle=Column(String(50), nullable=False)
    price=Column(Float(10,2), default=0)
    product_id=Column(Integer, ForeignKey("products.id"), index=True)
    # SKU específico (Ej: REM-OVERS-001-ROJO-L)
    sku=Column(String(50), nullable=False, unique=True, index=True)
    stock_current=Column(Integer, default=0, nullable=False)
    stock_min=Column(Integer,default=10, nullable=False)
    
    __table_args__=(
        CheckConstraint('stock_current >=0',name='check_stock_non_negative'),
    )
    
    product=relationship("Product", back_populates="variants")
    
    @property
    def stock_status(self)->str:
        #Calcula el estado del stock normal, alerta o agotado
        
        if self.stock_current==0:
            return "Agotado"
        
        elif self.stock_current<=self.stock_min:
            return "Alerta"
        else:
            return "Normal"
        
    def __repr__(self):
        return f"<Variant {self.sku} - Stock: {self.stock_current}>"