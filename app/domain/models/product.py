
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, CheckConstraint, Enum as SQLAlchemyEnum
from datetime import datetime
import enum
from app.core.database import Base

# class StockStatus(str, Enum):
#     NORMAL = "normal"
#     LOW = "low_stock"
#     OUT = "out_of_stock"
    
class Gender(str, enum.Enum):
    MAN= "hombre"
    WOMAN="mujer"
    CHILD="niño"
    UNISEX="unisex"
    ALL="todos"

class Product(Base):
    __tablename__="products"
    
    id= Column(Integer, index=True, primary_key=True)
    name=Column(String(255), nullable=False, index=True)
    description= Column(String(500))
    gender=Column(SQLAlchemyEnum(Gender),default=Gender.UNISEX, nullable=False)
    category_id= Column(Integer, ForeignKey("categories.id"))
    price=Column(Float(10,2))
    # SKU Base (ej: "REM-OVERS-001")
    
    sku_base= Column(String(50), index=True, nullable=False, unique=True)    
    created_at=Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,nullable=False)

    category=relationship("Category", back_populates="product")
    
    images=relationship("Images", back_populates="product", cascade="all, delete-orphan")
    variants=relationship("Variants", back_populates="product", cascade="all, delete-orphan")
    
    