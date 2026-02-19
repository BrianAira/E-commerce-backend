from typing import List, Optional
from sqlmodel import Session, select
from app.domain.models.variant import ProductVariant, ProductVariantCreate, ProductVariantUpdate
from app.application.ports.product_variant_port import IProductVariantRepository
from sqlalchemy.exc import SQLAlchemyError


class ProductVariantRepository(IProductVariantRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, variant: ProductVariantCreate) -> ProductVariant:
        try:
            
            db_variant = ProductVariant.from_orm(variant)
            self.session.add(db_variant)
            self.session.commit()
            self.session.refresh(db_variant)
            return db_variant
        except SQLAlchemyError as e:
            self.session.rollback()
            raise
            

    def get_by_id(self, variant_id: int) -> Optional[ProductVariant]:
        return self.session.get(ProductVariant, variant_id)

    def list_by_product(self, product_id: int) -> List[ProductVariant]:
        statement = select(ProductVariant).where(ProductVariant.product_id == product_id)
        return list(self.session.exec(statement))

    def update(self, variant_id: int, data: ProductVariantUpdate) -> Optional[ProductVariant]:
        db_variant = self.session.get(ProductVariant, variant_id)
        if not db_variant:
            return None

        try:
            for field, value in data.dict(exclude_unset=True).items():
                setattr(db_variant, field, value)

            self.session.add(db_variant)
            self.session.commit()
            self.session.refresh(db_variant)
            return db_variant
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def delete(self, variant_id: int) -> bool:
        db_variant = self.session.get(ProductVariant, variant_id)
        if not db_variant:
            return False
        try: 
            self.session.delete(db_variant)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            # return False
            raise

    def change_stock(self, variant_id:int, delta:int)->Optional[ProductVariant]:
        variant=self.get_by_id(variant_id)
        if not variant:
            return None
        new_stock=variant.stock +delta
        if new_stock<0:
            raise ValueError("Stock insuficiente")
        try:
            variant.stock=new_stock
            self.session.add(variant)
            self.session.commit()
            self.session.refresh(variant)
            return variant
        except SQLAlchemyError as e:
            self.session.rollback()
            raise
            # return None
        
    def find_by_attributes(self, product_id:int, size:int, color:str)->Optional[ProductVariant]:
        statement=(
            select(ProductVariant)
            .where(ProductVariant.product_id==product_id, 
                   ProductVariant.size==size,
                   ProductVariant.color==color
                   )
            )
        return self.session.exec(statement).first()