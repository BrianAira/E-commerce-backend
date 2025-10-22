from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.product_variants import (
    ProductVariant,
    ProductVariantCreate,
    ProductVariantUpdate,
)

class IProductVariantRepository(ABC):

    @abstractmethod
    def create(self, variant: ProductVariantCreate) -> ProductVariant:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, variant_id: int) -> Optional[ProductVariant]:
        raise NotImplementedError

    @abstractmethod
    def list_by_product(self, product_id: int) -> List[ProductVariant]:
        raise NotImplementedError

    @abstractmethod
    def update(self, variant_id: int, data: ProductVariantUpdate) -> Optional[ProductVariant]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, variant_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def change_stock(self, variant_id:int, delta:int)->Optional[ProductVariant]:
        raise NotImplementedError