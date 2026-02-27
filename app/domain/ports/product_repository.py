from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.models.product import Product
from app.domain.models.variant import VariantProduct
from app.domain.schemas.product import ProductCreate, ProductFilterParams, ProductUpdate


class IProductRepository(ABC):
    @abstractmethod
    def get_by_id(self, product_id:int)->Optional[Product]:
        pass
    
    # def get_by_sku(self, sku:str)->Product:
        # pass
    # @abstractmethod
    # def get_by_slug(self, slug:str)->Optional[Product]:
    #     pass
    
    @abstractmethod
    def list_filtered(self, params:ProductFilterParams)->List[Product]:
        pass
    
    @abstractmethod
    def create(self, data:ProductCreate)->Product:
        pass
    
    @abstractmethod
    def update_variant_stock(self, variant_id:int, quantity:int)->bool:
        pass
    
    @abstractmethod
    def update_product(self, product_id:int, data:ProductUpdate)->Product:
        pass
    
    # @abstractmethod
    # def get_variant_by_sku(self, sku:str)->Optional[VariantProduct]:
    #     pass
    
    