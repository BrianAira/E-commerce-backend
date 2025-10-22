from typing import List, Optional
from sqlmodel import Session, select
from app.domain.models.product_variants import ProductVariant, ProductVariantCreate, ProductVariantUpdate
from app.application.ports.product_variant_port import IProductVariantRepository


class ProductVariantRepository(IProductVariantRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, variant: ProductVariantCreate) -> ProductVariant:
        db_variant = ProductVariant.from_orm(variant)
        self.session.add(db_variant)
        self.session.commit()
        self.session.refresh(db_variant)
        return db_variant

    def get_by_id(self, variant_id: int) -> Optional[ProductVariant]:
        return self.session.get(ProductVariant, variant_id)

    def list_by_product(self, product_id: int) -> List[ProductVariant]:
        statement = select(ProductVariant).where(ProductVariant.product_id == product_id)
        return list(self.session.exec(statement))

    def update(self, variant_id: int, data: ProductVariantUpdate) -> Optional[ProductVariant]:
        db_variant = self.session.get(ProductVariant, variant_id)
        if not db_variant:
            return None

        for field, value in data.dict(exclude_unset=True).items():
            setattr(db_variant, field, value)

        self.session.add(db_variant)
        self.session.commit()
        self.session.refresh(db_variant)
        return db_variant

    def delete(self, variant_id: int) -> bool:
        db_variant = self.session.get(ProductVariant, variant_id)
        if not db_variant:
            return False
        self.session.delete(db_variant)
        self.session.commit()
        return True

    def change_stock(self, product_id:int, delta:int)->Optional[ProductVariant]:
        product=self.get_by_id(product_id)
        if not product:
            return None
        product.stock+=delta
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product