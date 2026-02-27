from typing import List, Optional
from sqlmodel import Session
from app.domain.models.variant import VariantProduct
from app.domain.ports.variant_repository import IVariantRepository
from app.domain.schemas.variant import VariantCreate, VariantUpdate


class SQLVariantRepository(IVariantRepository):
    def __init__(self, db:Session):
        self.db=db
    
    def get_by_id(self, variant_id:int):
        return self.db.query(VariantProduct).filter(VariantProduct.id==variant_id).first()
    
    def get_by_sku(self, sku:str)->Optional[VariantProduct]:
        return self.db.query(VariantProduct).filter(VariantProduct.sku==sku).first()
    
    def create_many(self, variants_data:List[VariantCreate])->List[VariantProduct]:
        new_variants=[]
        for v_data in variants_data:
            variant=VariantProduct(**v_data.model_dump())
            self.db.add(variant)
            new_variants.append(variant)
            
        self.db.commit()
        for v in new_variants:
            self.db.refresh(v)
        return new_variants
    
    def reduce_stock(self, variant_id:int, quantity:int)->bool:
        variant=self.get_by_id(variant_id)
        if not variant or variant.stock_current<quantity:
            return False
        
        variant.stock_current-=quantity
        self.db.commit()
        return True
    
    def increase_stock(self, variant_id:int, quantity:int)->bool:
        variant=self.get_by_id(variant_id)
        if not variant:
            return False
        
        variant.stock_current +=quantity
        self.db.commit()
        return True
    
    def update(self, variant_id:int, data:VariantUpdate)->Optional[VariantProduct]:
        variant=self.get_by_id(variant_id)
        if not variant:
            return None
        data=data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(variant, key, value)
            
        self.db.commit()
        self.db.refresh(variant)
        return variant                                                 

    def list_by_product(self, product_id:int)->List[VariantProduct]:
        return self.db.query(VariantProduct).filter(VariantProduct.product_id== product_id).all()
    
    def update_stock(self, variant_id:int, quantity_to_add:int)->VariantProduct:
        variant=self.get_by_id(variant_id)
        if not variant:
            raise ValueError("Variante no encontrada")
        variant.stock_current+=quantity_to_add
        
        if variant.stock_current<0:
            variant.stock_current=0
            
        self.db.commit()
        self.db.refresh(variant)
        return variant
    
    def list_low_stock(self, threshold:int)->List[VariantProduct]:
        return self.db.query(VariantProduct).filter(VariantProduct.stock_current<=threshold).all()
    
    def get_all_variants_with_products(self)->List[VariantProduct]:
        return self.db.query(VariantProduct).all()