from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session

from app.infrastructure.databases.database import get_session
from app.domain.services.order_item import OrderItemService
from app.domain.models.order_item import OrderItemRead, OrderItemCreate, OrderItemUpdate
from app.infrastructure.repositories.order_item import OrderItemRepository
from app.infrastructure.repositories.product import ProductRepository
from app.infrastructure.repositories.order import OrderRepository

router=APIRouter(prefix="/order_items", tags=["Order items"])

def get_order_item_service(session:Session=Depends(get_session)):
    order_item_repo=OrderItemRepository(session)
    order_repo=OrderRepository(session)
    product_repo=ProductRepository(session)
    return OrderItemService(order_repo,order_item_repo, product_repo, session)

@router.post(
    "/",
    response_model=OrderItemRead
    )
def add_item(orderItem:OrderItemCreate, service:OrderItemService=Depends(get_order_item_service)):
    try:
        return service.add_item(orderItem.order_id, orderItem.product_id, orderItem.quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
# @router.get(
#     "/{item_id}",
#     response_model=OrderItemRead
#     )
# def get_order_item(item_id:int, service:OrderItemService=Depends(get_order_item_service)):
#     order_item=service.get_order_item(item_id)
#     if not order_item:
#         raise HTTPException(status_code=404, detail="Item de orden no encontrado")
    
#     return order_item

@router.get(
    "/order/{order_id}",
    response_model=List[OrderItemRead],
    summary="Listar items de orden"
)
def list_order_items(order_id:int,service: OrderItemService=Depends(get_order_item_service)):
    return service.list_items(order_id)

@router.patch(
    "/{item_id}",
    response_model=OrderItemRead,
    summary="Actualizar item"
)
def update_quantity(item_id:int, item_data:OrderItemUpdate, service: OrderItemService=Depends(get_order_item_service)):
    
    try:
        return service.update_item_quantity(item_id,item_data.quantity,)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))    
   

@router.delete(
    "/{item_id}",
    summary="Eliminar item de orden"
)

def delete_order_item(item_id:int, service:OrderItemService=Depends(get_order_item_service)):
    deleted=service.remove_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item de orden no encontrada")
    return {"detail": "Item de orden eliminado con exito"}

@router.get(
    "/order/{order_id}",
    response_model=List[OrderItemRead],
    summary="Listar todos los items"
)
def list_items(order_id:int, service:OrderItemService=Depends(get_order_item_service)):
    return service.list_items(order_id)

