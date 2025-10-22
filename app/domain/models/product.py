# app/domain/models/product.py
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal

from app.domain.models.product_image import ProductImageRead
from app.domain.models.product_variants import ProductVariantRead

class ProductBase(SQLModel):
    name: str
    description: Optional[str] = None
    
    # sale_price:Decimal
    category:str=Field(min_length=2, max_length=100)
    gender:Optional[str]=Field(default=None, description="hombre, mujer, etc...")
    # image:str
    entry_price: Decimal
    min_wholesale_quantity:int=Field(default=6, description="Cantidad minima para aplicar precio mayorista")
    
    wholesale_price:Decimal=Field(gt=0, description="Precio mayorista")
    retail_price:Decimal=Field(gt=0, description="Precio minorista")
    stock: int=Field(default=1)
    
    is_active:bool=Field(default=True)

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    images:List["ProductImage"]=Relationship(back_populates="product")
    variants:List["ProductVariant"]=Relationship(back_populates="product")

    # Relación 1 a muchos con Cart: cada producto pertenece a un carrito
    
    cart_id: Optional[int] = Field(default=None, foreign_key="cart.id")
    # cart: Optional["Cart"] = Relationship(back_populates="product")


class ProductCreate(ProductBase):
    pass
    # cart_id: Optional[int] = None  # al crear un producto, puede asignarse a un carrito

class ProductRead(ProductBase):
    id: int
    images:Optional[List[ProductImageRead]]=[]
    variants:Optional[List[ProductVariantRead]]=[]
    
    # cart_id: Optional[int] = None
    
class ProductListRead(ProductBase):
    id:int
    main_image:Optional[str]=None
  
class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    # image:Optional[List[str]]=None
    entry_price: Optional[Decimal] = None
    # sale_price:Optional[Decimal]=None
    is_active:Optional[bool]=None
    stock: Optional[int] = None
    category:Optional[str]=None
    wholesale_price:Optional[Decimal]=None
    retail_price:Optional[Decimal]=None
    gender:Optional[str]=None 
    # cart_id: Optional[int] = None

# class ProductRead(ProductBase):
#     id: int
