from typing import List, Optional
from sqlmodel import Session
from app.domain.models.order import Order, OrderStatus
from app.domain.models.order_item import OrderItem
from app.domain.ports.order_repository import IOrderRepository


class SQLOrderRepository(IOrderRepository):
    def __init__(self, db:Session):
        self.db=db
        
    def create(self, user_id:int, total_amount:float, direction_id:int, items:List[dict])->Order:
        #Crea la order y sus detalles con una lista de diccionarios
        
        try:
            new_order=Order(
                user_id=user_id,
                total_amount=total_amount,
                direction_id=direction_id,
                status=OrderStatus.PENDING
            )
            self.db.add(new_order)
            self.db.flush()
            
            for item_data in items:
                order_item=OrderItem(
                    order_id=new_order.id,
                    variant_id=item_data["variant_id"],
                    quantity=item_data["quantity"],
                    price=item_data["price"]
                )
                self.db.add(order_item)
                
            self.db.commit()
            self.db.refresh(new_order)
            return new_order
        
        except Exception as e:
            self.db.rollback()
            raise e
        
    def get_by_id(self, order_id:int)->Optional[Order]:
        return self.db.query(Order).filter(Order.id==order_id).first()
    
    def get_orders_by_user_id(self, user_id:int)->List[Order]:
        return self.db.query(Order).filter(Order.user_id==user_id).order_by(Order.created_at.desc()).all()
    
    
    def get_all_orders(self)->List[Order]:
        return self.db.query(Order).order_by(Order.created_at.desc()).all()
    
    def update_status(self, order_id:int, mew_status:OrderStatus)->Order:
        order=self.get_by_id(order_id)
        if order:
            order.status=mew_status
            self.db.commit()
            self.db.refresh(order)
            
        return order
    