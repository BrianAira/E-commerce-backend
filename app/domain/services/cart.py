from typing import List, Optional
from sqlmodel import Session

from app.domain.models.cart import Cart, CartCreate, CartRead, CartUpdate
from app.application.ports.cart_port import ICartRepository
from app.application.ports.user_port import IUserRepository


class CartService:
    def __init__(self, cart_repo: ICartRepository, user_repo: IUserRepository, session: Session):
        self.cart_repo = cart_repo
        self.user_repo = user_repo
        self.session = session

    def create_cart(self, cart_data: CartCreate) -> CartRead:
        # 🔑 Regla: verificar que el usuario exista
        user = self.user_repo.get_by_id(cart_data.user_id)
        if not user:
            raise ValueError("User does not exist")

        # 🔑 Regla: solo un carrito por usuario
        existing_cart = self.cart_repo.get_by_user_id(cart_data.user_id)
        if existing_cart:
            raise ValueError("User already has a cart")

        cart = self.cart_repo.create(cart_data)
        return CartRead.from_orm(cart)

    def get_cart(self, cart_id: int) -> Optional[CartRead]:
        cart = self.cart_repo.get_by_id(cart_id)
        return CartRead.from_orm(cart) if cart else None

    def get_cart_by_user(self, user_id: int) -> Optional[CartRead]:
        cart = self.cart_repo.get_by_user_id(user_id)
        return CartRead.from_orm(cart) if cart else None

    def update_cart(self, cart_id: int, update_data: CartUpdate) -> Optional[CartRead]:
        cart = self.cart_repo.update(cart_id, update_data)
        return CartRead.from_orm(cart) if cart else None

    def delete_cart(self, cart_id: int) -> bool:
        return self.cart_repo.delete(cart_id)

    def list_carts(self) -> List[CartRead]:
        carts = self.cart_repo.list_all()
        return [CartRead.from_orm(c) for c in carts]
