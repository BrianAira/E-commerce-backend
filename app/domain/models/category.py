
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Category(Base):
    __tablename__="categories"
    
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String(255), unique=True, nullable=False)
    
    slug=Column(String(120), unique=True, index=True, nullable=False)
    
    
    products=relationship("Product", back_populates="category")