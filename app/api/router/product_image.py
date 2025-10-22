from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session

from app.infrastructure.databases.database import get_session
from app.domain.models.product_image import ProductImageCreate, ProductImageRead
from app.domain.services.product_image import ProductImageService
from app.infrastructure.repositories.product_image import ProductImageRepository
from app.infrastructure.repositories.product import ProductRepository
# Si usás autenticación basada en roles:
from app.infrastructure.security.dependencies import get_current_admin


router = APIRouter(prefix="/product-images", tags=["Product Images"])


# Dependencia para crear el servicio
def get_product_image_service(session: Session = Depends(get_session)) -> ProductImageService:
    image_repo = ProductImageRepository(session)
    product_repo = ProductRepository(session)
    return ProductImageService(image_repo, product_repo, session)


# -----------------------------
# 📌 Crear una nueva imagen
# -----------------------------
@router.post("/", response_model=ProductImageRead, status_code=status.HTTP_201_CREATED)
def create_product_image(
    image_data: ProductImageCreate,
    service: ProductImageService = Depends(get_product_image_service),
    admin=Depends(get_current_admin)  # Descomenta si querés restringir a admins
):
    try:
        return service.add_image(image_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# -----------------------------
# 📌 Listar imágenes por producto
# -----------------------------
@router.get("/product/{product_id}", response_model=List[ProductImageRead])
def list_product_images(
    product_id: int,
    service: ProductImageService = Depends(get_product_image_service)
):
    images = service.list_by_product(product_id)
    if not images:
        raise HTTPException(status_code=404, detail="No se encontraron imágenes para este producto")
    return images


# -----------------------------
# 📌 Eliminar imagen por ID
# -----------------------------
@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_image(
    image_id: int,
    service: ProductImageService = Depends(get_product_image_service),
    admin=Depends(get_current_admin)
):
    success = service.delete_image(image_id)
    if not success:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return {"detail": "Imagen eliminada correctamente"}
