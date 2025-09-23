from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session

from app.infrastructure.databases.database import get_session
from app.domain.models.cart import CartCreate, CartRead, CartUpdate
from app.infrastructure.repositories.cart import CartRepository
from app.infrastructure.repositories.user import UserRepository
from app.domain.services.cart import CartService


router = APIRouter(prefix="/carts", tags=["carts"])


def get_cart_service(session: Session = Depends(get_session)):
    cart_repo = CartRepository(session)
    user_repo = UserRepository(session)
    return CartService(cart_repo, user_repo, session)


@router.post("/", response_model=CartRead, status_code=status.HTTP_201_CREATED)
def create_cart(cart: CartCreate, service: CartService = Depends(get_cart_service)):
    try:
        return service.create_cart(cart)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{cart_id}", response_model=CartRead)
def get_cart(cart_id: int, service: CartService = Depends(get_cart_service)):
    cart = service.get_cart(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.get("/user/{user_id}", response_model=CartRead)
def get_cart_by_user(user_id: int, service: CartService = Depends(get_cart_service)):
    cart = service.get_cart_by_user(user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found for this user")
    return cart


@router.put("/{cart_id}", response_model=CartRead)
def update_cart(
    cart_id: int,
    update_data: CartUpdate,
    service: CartService = Depends(get_cart_service)
):
    cart = service.update_cart(cart_id, update_data)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(cart_id: int, service: CartService = Depends(get_cart_service)):
    ok = service.delete_cart(cart_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Cart not found")
