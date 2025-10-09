from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.order_item import OrderItem, OrderItemCreate, OrderItemUpdate, OrderItemRead

class IOrderItemRepository(ABC):
    
    @abstractmethod
    def create(self, item:OrderItemCreate)->OrderItem:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, item_id:int)->Optional[OrderItem]:
        raise NotImplementedError
     
    @abstractmethod
    def update(self,item_id:int, item_data:OrderItemUpdate)->OrderItem:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, item_id:OrderItem)->bool:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_order(self, order_id:int)->List[OrderItem]:
        raise NotImplementedError
    