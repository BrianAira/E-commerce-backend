from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.models.variant import VariantProduct
from app.domain.schemas.variant import VariantCreate, VariantUpdate


class IVariantRepository(ABC):
    @abstractmethod
    def get_by_id(self, variant_id:int)->Optional[VariantProduct]:
        pass
    
    @abstractmethod
    def get_by_sku(self, sku:str)->Optional[VariantProduct]:
        pass
    
    @abstractmethod
    def list_by_product(self, product_id:int)->List[VariantProduct]:
        pass
    
    #actualizacion manual de stock desde admin
    @abstractmethod
    def update_stock(self, variant_id:int, new_stock:int)->bool:
        pass
    
    @abstractmethod
    def list_low_stock(self, threshold:int)->List[VariantProduct]:
        pass
    
    #actualizar muchos stocks de una vez desde excel
    # @abstractmethod
    # def bulk_update_stock(self, updates:List[dict])->bool:
    #     pass 
    
    #Resta stock al confirmar una compra
    @abstractmethod
    def reduce_stock(self, variant_id:int, quantity:int)->bool:
        pass
    
    #devuelve stock al cancelar una orden
    @abstractmethod
    def increase_stock(self, variant_id:int, quantity:int)->bool:
        pass
    
    @abstractmethod
    def create_many(self, variants_data:List[VariantCreate])->List[VariantProduct]:
        pass
    
    @abstractmethod
    def update(self, variant_id:int, data:VariantUpdate)->VariantProduct:
        pass
    
    
    @abstractmethod
    def get_all_variants_with_products(self)->List[VariantProduct]:
        return self.db.query(VariantProduct).all()
    