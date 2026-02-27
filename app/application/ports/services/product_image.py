from typing import List
from sqlmodel import Session
from fastapi import HTTPException, status
from app.domain.models.image import ProductImage, ProductImageCreate, ProductImageRead
from app.application.ports.product_image_port import IProductImageRepository
from app.application.ports.product_port import IProductRepository


class ProductImageService:
    def __init__(self, image_repo: IProductImageRepository, product_repo: IProductRepository, session: Session):
        self.image_repo = image_repo
        self.product_repo = product_repo
        self.session = session

    def add_image(self, image_data: ProductImageCreate) -> ProductImageRead:
        # Validar producto existente
        product = self.product_repo.get_by_id(image_data.product_id)
        if not product:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Producto no encontrado")

        # Verificar si ya existe la imagen para ese producto
        existing = self.image_repo.find_by_url(image_data.url, image_data.product_id)
        if existing:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Esta imagen ya está asociada al producto")

        # Crear imagen nueva
        image = self.image_repo.create(image_data)
        return ProductImageRead.from_orm(image)


    def list_by_product(self, product_id: int) -> List[ProductImageRead]:
        images = self.image_repo.list_by_product(product_id)
        return [ProductImageRead.from_orm(i) for i in images]

    def delete_image(self, image_id: int) -> bool:
        return self.image_repo.delete(image_id)

    def set_main_image(self, product_id: int, image_id: int) -> ProductImageRead:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Producto no encontrado")

        success = self.image_repo.set_main_image(product_id, image_id)
        if not success:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Imagen no encontrada o error al actualizar")

        image = self.image_repo.get_by_id(image_id)
        return ProductImageRead.from_orm(image)
