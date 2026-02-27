from typing import List, Optional
from fastapi import HTTPException, status
from pymysql import IntegrityError
from sqlmodel import Session
from app.domain.models.variant import ProductVariantUpdate, ProductVariantRead, ProductVariantCreate
from app.application.ports.product_variant_port import IProductVariantRepository


class ProductVariantService:
    def __init__(self, repo: IProductVariantRepository, session: Session):
        self.repo = repo
        self.session = session

    def create_variant(self, data: ProductVariantCreate) -> ProductVariantRead:
        existing=self.repo.find_by_attributes(
            product_id=data.product_id,
            size=data.size,
            color=data.color
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una variante con ese color y talle para este producto"
            )
            
        if data.stock<0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El stock no puede ser negativo"
            )
        
        try:
            
            # if data.stock < 0:
                # raise ValueError("El stock no puede ser negativo")
                # raise HTTPException(status_code=400, detail="Stock invalido")
            variant = self.repo.create(data)
            return ProductVariantRead.from_orm(variant)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Ya existe esa variante")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno: {e}")

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
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Producto no encontrado o stock insuficiente")
        
        new_stock=variant.stock+delta
        if new_stock<0:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Stock insuficiente para realizar esta operacion")
        
        update_variant=self.repo.change_stock(variant_id, delta)
        return ProductVariantRead.from_orm(update_variant)
        # variant=self.repo.get_by_id(variant_id)
        # if not variant:
        #     return None
        # variant.stock+=quantity
        # updated=self.repo.update(variant_id, variant)
        
        # return ProductVariantRead.from_orm(updated)