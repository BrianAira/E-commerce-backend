from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session

from app.infrastructure.databases.database import get_session
from app.domain.services.order import OrderService
from app.domain.models.order import OrderCreate, OrderRead, OrderUpdate
from app.infrastructure.repositories.order import OrderRepository
from app.infrastructure.repositories.order_item import OrderItemRepository
from app.domain.models.status_update import StatusUpdate



router=APIRouter(prefix="/orders", tags=["Orders"])

def get_order_service(session:Session=Depends(get_session)):
    order_repo=OrderRepository(session)
    order_item_repo=OrderItemRepository(session)
    return OrderService(order_repo, order_item_repo,session)
 
@router.post(
    "/",
    response_model=OrderRead,
    summary="Crear orden"
)
def create_order(order:OrderCreate, service:OrderService=Depends(get_order_service)):
    return service.create_order(order)

@router.get(
    "/{order_id}",
    response_model=OrderRead,
    summary="TRaer orden por id"
)
def get_order(order_id:int, service:OrderService=Depends(get_order_service)):
    order=service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    return order

@router.get(
    "/",
    response_model=List[OrderRead],
    summary="Listar ordenes"
)
def list_orders(service:OrderService=Depends(get_order_service)):
    return service.list_orders()

@router.patch( ##No definido correctamente
    "/{order_id}",
    response_model=OrderRead,
    summary="actualizar orden"
)
def update_order(order_id:int, order_data:OrderUpdate, service:OrderService=Depends(get_order_service)):
    updated=service.update_order(order_id, order_data)
    
    if not updated:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return updated

@router.delete(
    "/{order_id}",
    summary="Eliminar orden"
    )
def delete_order(order_id:int, service:OrderService=Depends(get_order_service)):
    deleted=service.delete_order(order_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    return {"detail": "Orden eliminada con exito"}

@router.patch(
    "/{order_id}/status",
    response_model=OrderRead,
    summary="Cambiar estado de orden"
)
def change_order_status(order_id:int, new_status:StatusUpdate, service:OrderService=Depends(get_order_service)):
    # order=service.order_repo.get_by_id(order_id)
    # if not order:
    #     raise ValueError("Orden no encontrada")
    
    # order.status=new_status
    # updated=service.order_repo.update(order_id, order)
    # return OrderRead.from_orm(updated)
    
    try:
        return service.change_status(order_id, new_status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get(
    "/client/{client_id}",
    response_model=List[OrderRead],
    summary="Traer por cliente"
)

def get_by_client(client_id:int, service:OrderService=Depends(get_order_service)):
    return service.order_repo.get_by_client(client_id)