from typing import List, Optional
from sqlmodel import Session, select
from app.domain.models.order_item import OrderItem,OrderItemCreate
from app.application.ports.order_item_port import IOrderItemRepository

class OrderItemRepository(IOrderItemRepository):
    def __init__(self, session:Session):
        self.session=session
        
    def create(self, item:OrderItemCreate)->OrderItem:
        db_item=OrderItem.from_orm(item)
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return item
    
    def get_by_id(self, item_id:int)->Optional[OrderItem]:
        
        return self.session.get(OrderItem, item_id)
     
    def update(self, item_id:int, item_data:OrderItem)->Optional[OrderItem]:
        db_item=self.get_by_id(item_id)
        if not db_item:
            return None
        if item_data.quantity is not None:
            db_item.quantity=item_data.quantity
        if item_data.subtotal is not None:
            db_item.subtotal=item_data.subtotal
    
        for field, value in item_data.dict(exclude_unset=True).items():
            setattr(db_item, field, value)
            
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item
    
    def delete(self, item_id:int)->bool:
        item=self.get_by_id(item_id)
        if not item:
            raise False
        
        self.session.delete(item)
        self.session.commit()
        return True
    
    def get_by_order(self, order_id:int)->List[OrderItem]:
        statement=select(OrderItem).where(OrderItem.order_id==order_id)
        return self.session.exec(statement).all()