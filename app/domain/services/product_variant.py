from typing import List, Optional
from sqlmodel import Session
from app.domain.models.product_variants import ProductVariantUpdate, ProductVariantRead, ProductVariantCreate
from app.application.ports.product_variant_port import IProductVariantRepository


class ProductVariantService:
    def __init__(self, repo: IProductVariantRepository, session: Session):
        self.repo = repo
        self.session = session

    def create_variant(self, data: ProductVariantCreate) -> ProductVariantRead:
        if data.stock < 0:
            raise ValueError("El stock no puede ser negativo")

        variant = self.repo.create(data)
        return ProductVariantRead.from_orm(variant)

    def list_by_product(self, product_id: int) -> List[ProductVariantRead]:
        variants = self.repo.list_by_product(product_id)
        return [ProductVariantRead.from_orm(v) for v in variants]

    def update_variant(self, variant_id: int, data: ProductVariantUpdate) -> Optional[ProductVariantRead]:
        variant = self.repo.update(variant_id, data)
        return ProductVariantRead.from_orm(variant) if variant else None

    def delete_variant(self, variant_id: int) -> bool:
        return self.repo.delete(variant_id)
    
    # def get_by_id(self, variant_id:int):
    #     return self.repo.get_by_id

    def change_stock(self, variant_id:int, delta:int)->Optional[ProductVariantRead]:
        variant=self.repo.get_by_id(variant_id)
        if not variant:
            raise ValueError("Producto no encontrado o stock insuficiente")
        
        new_stock=variant.stock+delta
        if new_stock<0:
            raise ValueError("Stock insuficiente para realizar esta operacion")
        
        update_variant=self.repo.change_stock(variant_id, delta)
        return ProductVariantRead.from_orm(update_variant)
        # variant=self.repo.get_by_id(variant_id)
        # if not variant:
        #     return None
        # variant.stock+=quantity
        # updated=self.repo.update(variant_id, variant)
        
        # return ProductVariantRead.from_orm(updated)