from typing import List, Optional
from sqlmodel import Session, select

from app.domain.models.cart import Cart, CartCreate, CartUpdate
from app.application.ports.cart_port import ICartRepository


class CartRepository(ICartRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, cart: CartCreate) -> Cart:
        db_cart = Cart.from_orm(cart)  # convierte CartCreate → Cart
        self.session.add(db_cart)
        self.session.commit()
        self.session.refresh(db_cart)  # refresca con ID generado
        return db_cart

    def get_by_id(self, cart_id: int) -> Optional[Cart]:
        return self.session.get(Cart, cart_id)

    def get_by_user_id(self, user_id: int) -> Optional[Cart]:
        statement = select(Cart).where(Cart.user_id == user_id)
        return self.session.exec(statement).first()

    def update(self, cart_id: int, cart_data: CartUpdate) -> Optional[Cart]:
        db_cart = self.session.get(Cart, cart_id)
        if not db_cart:
            return None

        for key, value in cart_data.dict(exclude_unset=True).items():
            setattr(db_cart, key, value)

        self.session.add(db_cart)
        self.session.commit()
        self.session.refresh(db_cart)
        return db_cart

    def delete(self, cart_id: int) -> bool:
        db_cart = self.session.get(Cart, cart_id)
        if not db_cart:
            return False
        self.session.delete(db_cart)
        self.session.commit()
        return True

    def list_all(self) -> List[Cart]:
        return list(self.session.exec(select(Cart)))

    # def add_item(self,cart:Cart, product_id:int, quantity:int)->Cart:
    #     return cart
        
    # def remove_item(self, cart:Cart, product_id:int, quantity:int)->Cart:
    #     return cart
    
    # def update_item_quantity(self, cart:Cart, product_id:int, quantity:int)->Cart:
    #     return cart
    
    def clear_cart(self, cart:Cart)->Cart:
        return cart