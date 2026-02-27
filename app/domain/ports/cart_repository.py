from abc import ABC, abstractmethod
from typing import Optional

from app.domain.models.cart import Cart
from app.domain.models.cart_item import CartItem


class ICartRepository(ABC):
    
    @abstractmethod
    def get_by_user_id(self, user_id:int)->Optional[Cart]:
        pass
    
    @abstractmethod
    def create_cart(self, user_id:int)->Cart:
        pass
    
    @abstractmethod
    def add_or_update_item(self, cart_id:int, variant_id:int, quantity:int)->CartItem:
        pass
    
    @abstractmethod
    def remove_item(self, cart_id:int, variant_id:int)->bool:
        pass
    
    @abstractmethod
    def update_item_quantity(self, cart_id:int, variant_id:int, quantity:int)->Optional[CartItem]:
        pass
    
    @abstractmethod
    def clear_cart(self, cart_id:int)->None:
        pass
    
    @abstractmethod
    def get_by_id(self, cart_id:int)->Optional[Cart]:
        pass
    
    @abstractmethod
    def update_cart_total(cart_id:int, new_total:float)->Cart:
        pass
    
    