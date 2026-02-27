from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.models.order import Order, OrderStatus
from app.domain.schemas.order import OrderFilters


class IOrderRepository(ABC):
    
    @abstractmethod
    def create(self, order:Order)->Order:
        pass
    
    @abstractmethod
    def get_by_id(self, order_id:int)->Optional[Order]:
        pass
    
    @abstractmethod
    def list_by_user(self, user_id:int, skip:int=0, limit:int=10)->List[Order]:
        pass
    
    @abstractmethod
    def update_status(self, order_id:int, mew_status:OrderStatus)->Order:
        pass
    
    @abstractmethod
    def add_tracking_number(self, order_id:int, tracking_number:str)->Order:
        pass
    
    @abstractmethod
    def get_orders_by_user_id(self, user_id:int)->List[Order]:
        pass
    
    @abstractmethod
    def get_all_orders(self, filters:OrderFilters)->List[Order]:
        pass