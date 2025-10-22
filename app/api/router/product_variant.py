from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session

from app.domain.models.stockChange import StockChange
from app.infrastructure.databases.database import get_session
from app.infrastructure.repositories.product_variant import ProductVariantRepository
from app.domain.services.product_variant import ProductVariantService
from app.domain.models.product_variants import ProductVariantCreate, ProductVariantRead, ProductVariantUpdate
from app.infrastructure.security.dependencies import get_current_admin

router = APIRouter(prefix="/product-variants", tags=["Product Variants"])
 
def get_variant_service(session: Session = Depends(get_session)):
    repo = ProductVariantRepository(session)
    return ProductVariantService(repo, session)


@router.post("/", response_model=ProductVariantRead, status_code=status.HTTP_201_CREATED)
def create_variant(
    data: ProductVariantCreate,
    service: ProductVariantService = Depends(get_variant_service),
    admin=Depends(get_current_admin)
):
    return service.create_variant(data)


@router.get("/product/{product_id}", response_model=List[ProductVariantRead])
def list_variants(product_id: int, service: ProductVariantService = Depends(get_variant_service)):
    return service.list_by_product(product_id)


@router.put("/{variant_id}", response_model=ProductVariantRead)
def update_variant(
    variant_id: int,
    data: ProductVariantUpdate,
    service: ProductVariantService = Depends(get_variant_service),
    admin=Depends(get_current_admin)
):
    variant = service.update_variant(variant_id, data)
    if not variant:
        raise HTTPException(status_code=404, detail="Variante no encontrada")
    return variant


@router.delete("/{variant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_variant(
    variant_id: int,
    service: ProductVariantService = Depends(get_variant_service),
    admin=Depends(get_current_admin)
):
    ok = service.delete_variant(variant_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Variante no encontrada")


@router.patch("/{variant_id}/change-stock", response_model=ProductVariantRead)
def change_stock(
    variant_id:int,
    quantity:StockChange,
    service:ProductVariantService=Depends(get_variant_service),
    admin=Depends(get_current_admin)
):
    variant=service.change_stock(variant_id, quantity.delta)
    if not variant:
        raise HTTPException(status_code=404, detail="Variant no encontrada")
    return variant