from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session

from app.infrastructure.databases.database import get_session
from app.domain.models.cart import CartCreate, CartRead, CartUpdate
from app.domain.models.cart_item import CartItemRead, CartItemCreate, CartItemUpdate
from app.infrastructure.repositories.cart import CartRepository
from app.infrastructure.repositories.user import UserRepository
from app.infrastructure.repositories.cart_item import CartItemRepository
from app.infrastructure.repositories.product import ProductRepository
from app.domain.services.cart_item import CartItemService

router=APIRouter(prefix="/cart-items", tags=["carts"])

def get_cart_item_service(session:Session=Depends(get_session)):
    cart_repo=CartRepository(session)
    cart_item_repo=CartItemRepository(session)
    product_repo=ProductRepository(session)
    return CartItemService(cart_item_repo,cart_repo , product_repo,session)

@router.post(
    "/{cart_id}/items",
    response_model=CartItemRead,
    status_code=status.HTTP_201_CREATED
)
def add_item_to_cart(
    item:CartItemCreate,
    service:CartItemService=Depends(get_cart_item_service)
    # cart_id:int, item:CartItemCreate, service:CartService=Depends(get_cart_service)
):
    try:
        return service.add_item(item.cart_id, item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/cart/{cart_id}",
    response_model=List[CartItemRead]
)
def list_cart_items(
    cart_id:int,
    service:CartItemService=Depends(get_cart_item_service)
):
    
    return service.list_items(cart_id)

@router.put(
    "/{item_id}",
    response_model=CartItemRead
)
def update_item_in_cart(
    item_id:int,
    update_data:CartItemUpdate,
    service:CartItemService=Depends(get_cart_item_service)
):
    try:
        return service.update_item_quantity(item_id, update_data.quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_item_from_cart(
   
    item_id:int,
    service:CartItemService=Depends(get_cart_item_service)
):
    success=service.remove_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item no encontrado")
        