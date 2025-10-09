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
from app.domain.services.cart import CartService


router = APIRouter(prefix="/carts", tags=["carts"])


def get_cart_service(session: Session = Depends(get_session)):
    cart_repo = CartRepository(session)
    user_repo = UserRepository(session)
    cart_item_repo=CartItemRepository(session)
    product_repo=ProductRepository(session)
    return CartService(cart_repo, user_repo, session, cart_item_repo, product_repo)

#Crear carrito 
@router.post("/", response_model=CartRead, status_code=status.HTTP_201_CREATED)
def create_cart(cart: CartCreate, service: CartService = Depends(get_cart_service)):
    try:
        return service.create_cart(cart)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Traer carrito por id
@router.get("/{cart_id}", response_model=CartRead)
def get_cart(cart_id: int, service: CartService = Depends(get_cart_service)):
    cart = service.get_cart(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

#Traer carrito por id de usuario
@router.get("/user/{user_id}", response_model=CartRead)
def get_cart_by_user(user_id: int, service: CartService = Depends(get_cart_service)):
    cart = service.get_cart_by_user(user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found for this user")
    return cart

#Actualizar carrito por id
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

#Eliminar carrito
@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(cart_id: int, service: CartService = Depends(get_cart_service)):
    ok = service.delete_cart(cart_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Cart not found")
#Agregar item al carrito

#Borrar item de carrito
@router.delete(
    "/{cart_id}/items",
    response_model=CartRead
)
def clear_cart(cart_id:int, service:CartService=Depends(get_cart_service)):
    try:
        return service.clear_cart(cart_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

