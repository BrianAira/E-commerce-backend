from abc import ABC, abstractmethod

from app.domain.models.order import Order


class IPaymentRepository(ABC):
    @abstractmethod
    def create_payment_preference(self, order_data:Order)->str:
        pass
    
    @abstractmethod
    def get_payment_details(self, payment_id:str)->dict:
        pass
    
    