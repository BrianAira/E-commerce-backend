from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api.dependencies.dependencies import get_payment_repo, get_payment_service
from app.application.services.mercado_pago import MercadoPagoService
from app.core.database import get_db
from app.core.security import get_current_admin_user, get_current_user
from app.domain.models.order import OrderStatus
from app.domain.models.user import User, UserRole
from app.domain.ports.payment_repository import IPaymentRepository
from app.domain.schemas.order import CheckoutResponse, OrderCreate, OrderFilters, OrderResponse
from app.infrastructure.external_apis.mercadopago_repository import MercadoPagoRepository
from app.infrastructure.repositories.cart import SQLCartRepository
from app.infrastructure.repositories.order import SQLOrderRepository
from app.infrastructure.repositories.product import SQLProductRepository
from app.infrastructure.repositories.user import SQLUserRepository
from app.infrastructure.repositories.variant_repository import SQLVariantRepository
from app.application.services.order import OrderService
from app.core.config import settings

router=APIRouter(
    prefix="/orders",
    tags=["Orders"]
)
#Dependencia de servicio de ordenes
def get_order_service(
    db:Session=Depends(get_db),
    payment_service:MercadoPagoService=Depends(get_payment_service)
    # payment_repo:IPaymentRepository=Depends(get_payment_repo)
    )->OrderService:
    return OrderService(
        order_repo=SQLOrderRepository(db),
        cart_repo=SQLCartRepository(db),
        variant_repo=SQLVariantRepository(db),
        user_repo=SQLUserRepository(db),
        product_repo=SQLProductRepository(db),
        payment_repo=payment_service.payment_provider
    )
    
@router.post(
    "/", 
    response_model=CheckoutResponse, 
    status_code=status.HTTP_201_CREATED)
def checkout(
    order_data:OrderCreate,
    current_user:User=Depends(get_current_user),
    service:OrderService=Depends(get_order_service),
    # payment_service:MercadoPagoService=Depends(get_payment_service)
):
    try:
        #Logica de negocio para crear la orden
        result= service.checkout(
            user_id=current_user.id,
            direction_id=order_data.shipping_address_id
        )
        
        order=result["order"]
        link=result["payment_url"]
        #Generacion del link de mp usando la orden recien creada
        # payment_url=payment_service.start_checkout (order.id, settings.MP_WEBHOOK_URL)
        
        return{
            "order_id":order.id,
            "total_amount":order.total_amount,
            "status":order.status,
            "payment_url":link
        }
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    #Consulta de errores
@router.get(
    "/my-orders", 
    response_model=List[OrderResponse]
    )
def get_my_orders(
    current_user:User=Depends(get_current_user),
    service:OrderService=Depends(get_order_service)
):
    return service.get_orders_by_user_id(current_user.id)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order_detail(
    order_id:int,
    current_user:User=Depends(get_current_user),
    service:OrderService=Depends(get_order_service)
):
    order=service.get_order_by_id(order_id)
    if not order or (order.user_id != current_user.id and not current_user.role== "admin"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return order


@router.get("/admin/all", response_model=List[OrderResponse])
def list_all_orders(
    admin:User=Depends(get_current_admin_user),
    service:OrderService=Depends(get_order_service),
    filters:OrderFilters=Depends()
):
    return service.get_all(filters) 

@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id:int,
    admin:User=Depends(get_current_admin_user),
    service:OrderService=Depends(get_order_service)
):
    
    try:
        return service.cancel_order(order_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id:int,
    new_status:OrderStatus,
    service:OrderService=Depends(get_order_service),
    current_admin:User=Depends(get_current_admin_user)
):
    try:
        return service.update_order_status(order_id, new_status)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    