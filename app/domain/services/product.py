from typing import List, Optional
from app.domain.models.product import Product, ProductCreate, ProductUpdate, ProductRead
from app.application.ports.product_port import IProductRepository
from decimal import Decimal
from sqlmodel import Session

class ProductService:
    def __init__(self, repository: IProductRepository, session:Session):
        self.repository = repository
        self.session=session

    # Crear producto
    def create_product(self, product_data: ProductCreate) -> ProductRead:
        if not product_data.name or product_data.name.strip() == "":
            raise ValueError("El nombre del producto no puede estar vacío")
        
        if product_data.sale_price is None or product_data.entry_price is None:
            raise ValueError("Debe especificarse el precio de entrada y de venta")
        
        if product_data.entry_price <Decimal("0") or product_data.sale_price<Decimal("0"):
            raise ValueError("Los precios no pueden ser negativos")
        
        if product_data.stock is None or product_data.stock<0:
            raise ValueError("El stock no puede ser negativo")
        
        existing=self.repository.get_by_name(product_data.name)
        if existing:
            raise ValueError("Ya existe un producto con ese nombre")
        
        prod=self.repository.create(product_data)

        return ProductRead.from_orm(prod)
    
    def get_by_id(self, product_id:int)->Optional[ProductRead]:
        prod=self.repository.get_by_id(product_id)
        return ProductRead.from_orm(prod) if prod else None
    
    def list_products(self, name:Optional[str]=None, category:Optional[str]=None)->List[ProductRead]:
        if name:
            return [ProductRead.from_orm(p) for p in self.repository.get_by_name(name)]
        if category:
            return [ProductRead.from_orm(p) for p in self.repository.get_by_category(category)]
        
        prods=self.repository.get_all()
        
        return [ProductRead.from_orm(p) for p in prods]
    
    
    def update_product(self, product_id:int, update_data:ProductUpdate)->Optional[ProductRead]:
        product=self.repository.get_by_id(product_id)
        if not product:
            return None
        
        if update_data.entry_price is not None and update_data.entry_price <Decimal("0"):
            raise ValueError("Precio de venta no puede ser negativo")
        
        if update_data.sale_price is not None and update_data.sale_price< Decimal("0"):
            raise ValueError("Precio de venta no puede ser negativo")
        
        if update_data.stock is not None and update_data.stock <0:
            raise ValueError("stock no puede ser negativo") 
        
        for field, val in update_data.dict(exclude_unset=True).items():
            setattr(product, field, val)
            
        updated=self.repository.update(product)
        
        return ProductRead.from_orm(updated) 
    
    def delete_product(self, product_id:int)->bool:
        product=self.repository.get_by_id(product_id)
        
        if not product:
            return False
        
        return self.repository.delete(product_id)
    
    def change_stock(self, product_id:int, delta:int)->Product:
        
       
        updated=self.repository.adjust_stock(product_id, delta)
        if not updated:
            raise ValueError("Producto no encontrado o stock insuficiente")
        return ProductRead.from_orm(updated)
    
    