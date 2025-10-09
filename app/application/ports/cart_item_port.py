from typing import List, Optional
from abc import ABC, abstractmethod
from app.domain.models.cart_item import CartItem, CartItemCreate, CartItemUpdate

class ICartItemRepository(ABC):
    @abstractmethod
    def create(self, item:CartItemCreate)->CartItem:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, item_id:int)->Optional[CartItem]:
        raise NotImplementedError
    
    @abstractmethod
    def list_by_cart_id(self, cart_id:int)->List[CartItem]:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, item_id:int, item_data:CartItemUpdate)->Optional[CartItem]:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, item_id:int)->bool:
        raise NotImplementedError
    