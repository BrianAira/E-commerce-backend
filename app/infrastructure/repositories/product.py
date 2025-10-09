from typing import List, Optional 
from sqlmodel import Session , select 
from app.application.ports.product_port import IProductRepository
from app.domain.models.product import Product, ProductCreate


class ProductRepository(IProductRepository):
    def __init__ (self, session:Session):
        self.session= session

    def create(self, product:ProductCreate)-> Product: 
        db_product= Product.from_orm(product)
        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return db_product
        
    def get_by_id(self, product_id:int)->Optional[Product]:
        return self.session.get(Product, product_id)
    
    def update(self, product:Product)->Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product
    
    def get_all(self)->List[Product]:
        return list(self.session.exec(select(Product)))
    
    def delete(self, product_id:int)->bool:
        product=self.get_by_id(product_id)
        if not product:
            return False
        self.session.delete(product)
        self.session.commit()
        return True
        
    def get_by_name(self, product_name:str)->List[Product]:
        statement=select(Product).where(Product.name==product_name)
        return list(self.session.exec(statement))
    
    def adjust_stock(self, product_id:int, delta:int)->Optional[Product]:
        product=self.get_by_id(product_id)
        if not product:
            return None
        product.stock+=delta
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product
    
    def get_by_category(self, product_category:str)->List[Product]:
        
        statement=select(Product).where(Product.category==product_category)
        return list(self.session.exec(statement))
        # return super().get_by_category(product_category)    
        
