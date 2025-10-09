from typing import List, Optional
from sqlmodel import Session, select
from app.domain.models.order import Order, OrderUpdate, OrderCreate
from app.application.ports.order_port import IOrderRepository

class OrderRepository(IOrderRepository):
    def __init__(self, session:Session):
        self.session=session
        
    def create(self, order:OrderCreate)->Order:
        db_order=Order.from_orm(order)
        self.session.add(db_order)
        self.session.commit()
        self.session.refresh(db_order)
        return db_order
    
    def get_by_id(self, order_id:int)->Optional[Order]:
        return self.session.get(Order, order_id)
    
    def update(self, order_id:int, order:OrderUpdate)->Optional[Order]:
        db_order=self.session.get(Order, order_id)
        if not db_order:
            return None
        for field, value in order.dict(exclude_unset=True).items():
            setattr(db_order, field, value)
            
        self.session.add(db_order)
        self.session.commit()
        self.session.refresh(db_order)
        return db_order
    
    def delete(self, order_id:int)->bool:
        order=self.get_by_id(order_id)
        if not order:
            return False
        self.session.delete(order)
        self.session.commit()
        return True
    
    def get_all(self)->List[Order]:
        statement=select(Order)
        return self.session.exec(statement).all()
    
    def get_by_client(self, client_id:int)->List[Order]:
        statement=select(Order).where(Order.client_id==client_id)
        return self.session.exec(statement).all()