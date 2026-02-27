

from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class ProductImageBase(SQLModel):
    url:str
    is_main:bool=Field(default=False)
    alt_text:Optional[str]=None
    
    
class ProductImage(ProductImageBase, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    product_id:int=Field(foreign_key="product.id")
    
    product:Optional["Product"]=Relationship(back_populates="images")
    
class ProductImageCreate(ProductImageBase):
    product_id:int
    
class ProductImageRead(ProductImageBase):
    product_id:int
    id:int
    model_config={
        "from_attributes": True
    }
    
class ProductImageUpdate(SQLModel):
    url:Optional[str]=None
    is_main:Optional[bool]=None
    alt_text:Optional[str]=None
    Product_id:Optional[int]=None
    
    
    
# from sqlalchemy.orm import relationship
# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from app.core.database import Base


# class Image(Base):
#     __tablename__="images"
    
#     id=Column(Integer, primary_key=True, index=True)
#     product_id=Column(Integer, ForeignKey("products.id"), nullable=False)
#     url=Column(String(500), nullable=False)
#     is_main=Column(Boolean, default=False)
#     position=Column(Integer, nullable=True)
    
#     product=relationship("Product", back_populates="images")