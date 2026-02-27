# app/application/ports/product_image_port.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.image import ProductImage, ProductImageCreate

class IProductImageRepository(ABC):
    @abstractmethod
    def create(self, image: ProductImageCreate) -> ProductImage:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, image_id: int) -> Optional[ProductImage]:
        raise NotImplementedError

    @abstractmethod
    def list_by_product(self, product_id: int) -> List[ProductImage]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, image_id: int) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_url(self, url: str, product_id: int) -> Optional[ProductImage]:
        raise NotImplementedError

    @abstractmethod
    def set_main_image(self, product_id: int, image_id: int) -> bool:
        raise NotImplementedError