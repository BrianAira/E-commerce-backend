from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.order import Order, OrderCreate, OrderRead, OrderUpdate

class IOrderRepository(ABC):
    
    @abstractmethod 
    def create(self, order:OrderCreate)->Order:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, order_id:int)->Optional[Order]:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, order:OrderUpdate, order_id:int)->Order:
        raise NotImplementedError
     
    @abstractmethod
    def delete(self, order_id:int)->bool:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self)->List[Order]:
        raise NotImplementedError
     
    @abstractmethod
    def get_by_client(self, client_id:int)->List[Order]:
        raise NotImplementedError