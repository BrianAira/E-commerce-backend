import json
from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlmodel import Session

from app.core.database import get_db
from app.core.security import get_current_admin_user
from app.domain.ports.category_repository import ICategoryRepository
from app.domain.ports.image_repository import IImageRepository
from app.domain.schemas.product import ProductFilterParams, ProductResponse
from app.domain.schemas.variant import VariantCreate, VariantResponse
from app.infrastructure.repositories.category import SQLCategoryRepository
from app.infrastructure.repositories.product import SQLProductRepository
from app.infrastructure.repositories.variant_repository import SQLVariantRepository
from app.domain.schemas.product import ProductCreate, ProductUpdate
from app.application.services.product import ProductService


router= APIRouter(prefix="/products", tags=["Products"])

def get_product_service(db:Session=Depends(get_db)):
    
    product_repo=SQLProductRepository(db)
    variant_repo=SQLVariantRepository(db)
    category_repo=SQLCategoryRepository(db)
    return ProductService(product_repo, variant_repo, category_repo)

@router.get(
    "/",
    response_model=List[ProductResponse],
    
)
def list_products(
    categories:Optional[List[str]]=Query(None, description="Filtrar"),
    price_min:Optional[float]=Query(None, ge=0),
    price_max:Optional[float]=Query(None),
    search:Optional[str]=Query(None, description="Busqueda por nombre"),
    # sort_by:Optional[str]=Query(None, description="Campo, price, created at"),
    order:Optional[str]=Query("asc", description="asc o desc"),
    service:ProductService=Depends(get_product_service)
        
):
    filters=ProductFilterParams(
        categories=categories,
        price_min=price_min,
        price_max=price_max,
        search=search,
        # sort_by=sort_by,
        order=order
    )
    return service.search_products(filters)
    # return service.get_filtered_products(filters)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id:int, service:ProductService=Depends(get_product_service)):
    
    product=service.get_product_details(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product no encontrado"
        )
    return product

@router.post(
    "/", 
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    #Dependencia en decorador, poner en funcion si se trabaja con sus datos
    dependencies=[Depends(get_current_admin_user)]
    )
async def create_product(
    # product_data:str=Form(..., description="JSON string con datos del producto"),
    #Mandar json de imagenes y producto por separado para manejar las imagenes con algun servicio
    # images:List[UploadFile]=File(...,description="Lista de imagenes (archivos binarios)"),
    product_data:ProductCreate,
    service:ProductService=Depends(get_product_service)
    
):
    try:
    #     #Parsear json manualmente desde el formulario
    #     data_dict=json.loads(product_data)
    #     product_create=ProductCreate(**data_dict)
        
    #     #Procesar imagenes subidas a bytes para el servicio
    #     image_bytes_list=[]
    #     for img in images:
    #         content=await img.read()
    #         image_bytes_list.append(content)
            
        # return service.create_product(product_create, image_bytes_list)

    
    # except json.JSONDecodeError:
    #     raise HTTPException(status_code=400, detail="El campo product_data debe ser un json valido")
        return service.create_product(product_data)   
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,  detail=str(e))
         
@router.patch(
    "/{product_id}", 
    response_model=ProductResponse,
    dependencies=[Depends(get_current_admin_user)]
    )
def update_product(
    product_id:int,
    product_data:ProductUpdate,
    service:ProductService=Depends(get_product_service)
):
    product=service.update_product(product_id, product_data)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produco no encontrado")
    return product

@router.post(
    "/{product_id}/images", 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)]
    )
def add_images_to_product(
    product_id:int,
    image_urls:List[str],
    service:ProductService=Depends(get_product_service)
):
    try:
        return service.add_product_images(product_id, image_urls)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)]
)
def delete_product(product_id:int, service:ProductService=Depends(get_product_service)):
    success=service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se pudo eliminar el producto")
    return None
 
 
@router.post(
    "/{product_id}/variant", 
    response_model=VariantResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)]
    )
def add_variant_to_product(
    product_id:int,
    variant_data:VariantCreate,
    service:ProductService=Depends(get_product_service)
):
    try:
        return service.add_new_variant(product_id,variant_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    
@router.patch(
    "/variants/{variant_id}/add-stock",
    dependencies=[Depends(get_current_admin_user)]
    )
def add_stock(
    variant_id:int,
    quantity:int,
    service:ProductService=Depends(get_product_service)
):
    try:
        return service.add_stock_to_variant(variant_id, quantity)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.get(
    "/inventory/status-report",
    dependencies=[Depends(get_current_admin_user)])
def get_inventory_report(service:ProductService=Depends(get_product_service)):
    return service.get_inventory_status_report()

