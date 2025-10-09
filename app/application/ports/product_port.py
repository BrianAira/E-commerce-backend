from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.product import Product, ProductCreate, ProductRead

class IProductRepository(ABC):
    
    @abstractmethod 
    def create(self, product:ProductCreate)-> Product: 
        raise NotImplementedError 
    
    @abstractmethod
    def get_by_id(self, product_id:int)->Optional[Product]:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, product:Product)->Product:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self)->List[Product]:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, product_id:int)->bool:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_name(self,product_name:str)->List[Product]:
        raise NotImplementedError
        
    @abstractmethod
    def get_by_category(self,product_category:str )->List[Product]:
        raise NotImplementedError
    
    @abstractmethod 
    def adjust_stock(self,product_id:int, delta:int)->Optional[Product]:
        raise NotImplementedError