from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session

from app.domain.models.product import Product, ProductCreate, ProductListRead, ProductRead, ProductUpdate
from app.domain.services.product import ProductService
from app.infrastructure.repositories.product import ProductRepository
from app.infrastructure.databases.database import get_session  # <- tu función para obtener Session
from app.domain.models.stockChange import StockChange
from app.infrastructure.security.dependencies import get_current_admin

router = APIRouter(prefix="/products", tags=["Products"])


def get_product_service(session: Session = Depends(get_session)) -> ProductService:
    repository = ProductRepository(session)
    return ProductService(repository, session)



@router.post("/", response_model=ProductRead, summary="Crear producto")
def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service),
    admin=Depends(get_current_admin)
):
    return service.create_product(product)

@router.get(
    "/{product_id}",
    response_model=ProductRead,
    summary="Traer producto por id"
)
def get_product(product_id:int, service:ProductService=Depends(get_product_service)):
    product=service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.get(
    "/",
    response_model=List[ProductListRead],
    summary="listar todos los productos"
    )
def list_products(
    search:Optional[str]=Query(None, description="Buscar por nombre"),
    category:Optional[str]=Query(None, description="Filtrar por categorya"),
    service:ProductService=Depends(get_product_service)
):
    return service.list_products(search, category)

@router.put(
    "/{product_id}",
    response_model=ProductRead,
    summary="Actualizar product"
)
def update_product(
    product_id:int,
    update_data:ProductUpdate,
    service:ProductService=Depends(get_product_service),
    admin=Depends(get_current_admin)
):
    updated=service.update_product(product_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated

@router.delete(
    "/{id_product}",
    response_model=dict
)
def delete_product(
    id_product:int, 
    service:ProductService=Depends(get_product_service),
    admin=Depends(get_current_admin)
    ):
    success= service.delete_product(id_product)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrad")
    return {"ok": True, "message":"Producto eliminado con exito"}

@router.patch(
    "/{product_id}/stock",
    response_model=ProductRead,
    summary="Actualizar stock"
)
def change_stock(
    product_id:int,
    delta:StockChange,
    service:ProductService=Depends(get_product_service),
    admin=Depends(get_current_admin)
):
    try:
        
        return service.change_stock(product_id, delta.delta)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
# @router.post("/{product_id}/images")
# def add_image_to_product(product_id:int, data_img:CreateImage):
    