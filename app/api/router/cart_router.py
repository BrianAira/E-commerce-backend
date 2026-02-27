from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.domain.models.user import User
from app.domain.schemas.cart import CartItemUpdate, CartResponse
from app.infrastructure.repositories.cart import SQLCartRepository
from app.infrastructure.repositories.variant_repository import SQLVariantRepository
from app.application.services.cart import CartService
from app.domain.schemas.cart import CartItemCreate


router=APIRouter(
    prefix="/cart", 
    tags=["Cart"],
    dependencies=[Depends(get_current_user)]
    )

def get_cart_services(db:Session=Depends(get_db))->CartService:
    cart_repo=SQLCartRepository(db)
    variant_repo=SQLVariantRepository(db)
    return CartService(cart_repo, variant_repo)


@router.get("/", response_model=CartResponse)
def get_my_cart(
    current_user:User=Depends(get_current_user),
    service:CartService=Depends(get_cart_services)
):
    return service.get_or_create_cart(current_user.id)

@router.post("/items", response_model=CartResponse)
def add_item_to_cart(
    item_data:CartItemCreate,
    current_user=Depends(get_current_user),
    service:CartService=Depends(get_cart_services)
):
    try:
        return service.add_product_to_cart(
            user_id=current_user.id,
            variant_id=item_data.variant_id,
            quantity=item_data.quantity
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
@router.patch("/items/{variant_id}", response_model=CartResponse)
def update_item_quantity(
    variant_id:int,
    update_data:CartItemUpdate,
    current_user=Depends(get_current_user),
    service:CartService=Depends(get_cart_services)
):
    try:
    
        return service.update_item_quantity(
            user_id=current_user.id,
            variant_id=variant_id,
            new_quantity=update_data.quantity
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.delete(
    "/items/{variant_id}", 
    status_code=status.HTTP_204_NO_CONTENT)
def remove_item_from_cart(
    variant_id:int,
    current_user=Depends(get_current_user),
    service:CartService=Depends(get_cart_services)
):
    service.remove_item_from_cart(current_user.id, variant_id)
    return None

@router.delete(
    "/", 
    status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    current_user=Depends(get_current_user),
    service:CartService=Depends(get_cart_services)
):
    service.clear_cart(current_user.id)
    return None