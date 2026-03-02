from datetime import datetime, time
from typing import List, Optional
from sqlmodel import Session
from app.domain.models.order import Order, OrderStatus
from app.domain.models.order_item import OrderItem
from app.domain.ports.order_repository import IOrderRepository
from app.domain.schemas.order import OrderFilters


class SQLOrderRepository(IOrderRepository):
    def __init__(self, db:Session):
        self.db=db
        
    def create(self, user_id:int, total_amount:float, shipping_address_snapshot:int, items:List[dict])->Order:
        #Crea la order y sus detalles con una lista de diccionarios
        
        try:
            new_order=Order(
                user_id=user_id,
                total_amount=total_amount,
                shipping_address_snapshot=shipping_address_snapshot,
                status=OrderStatus.PENDING
            )
            self.db.add(new_order)
            self.db.flush()
            
            for item_data in items:
                order_item=OrderItem(
                    order_id=new_order.id,
                    variant_id=item_data["variant_id"],
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"]
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
        return self.db.query(Order).filter(Order.user_id==user_id).order_by(Order.order_date.desc()).all()
    
    
    def get_all_orders(self, filters:OrderFilters)->List[Order]:
        query=self.db.query(Order)
        
        if filters.status:
            query=query.filter(Order.status==filters.status)
            
        if filters.location:
            query=query.filter(Order.shipping_address_snapshot.ilike(f"%{filters.location}%"))
            
        if filters.postal_code:
            
            query=query.filter(Order.shipping_address_snapshot.ilike(f"%{filters.postal_code}%"))
        
        if filters.start_date:
            start_dt=datetime.combine(filters.start_date, time.min)
            query=query.filter(Order.order_date>=start_dt)
            
        if filters.end_date:
            end_dt=datetime.combine(filters.end_date, time.max)
            query=query.filter(Order.order_date<=end_dt)
        
        return query.order_by(Order.order_date.desc()).all()
        # return self.db.query(Order).order_by(Order.order_date.desc()).all()
    
    def update_status(self, order_id:int, new_status:OrderStatus)->Order:
        order=self.get_by_id(order_id)
        if order:
            order.status=new_status
            self.db.commit()
            self.db.refresh(order)
            
        return order
    
    def add_tracking_number(self, order_id:int, tracking_number:str)->Order:
        order=self.db.query(Order).filter(Order.id==order_id).first()
        if not order:
            raise ValueError(f"No se encontro la orden con ID {order_id}")
        
        order.tracking_number=tracking_number
        
        order.status=OrderStatus.SHIPPED
        try:
            self.db.commit()
            self.db.refresh(order)
            return order
        except Exception as e:
            self.db.rollback()
            raise e
        # return super().add_tracking_number(order_id, tracking_number)
        
    def list_by_user(self, user_id:int, skip:int = 0, limit:int = 10)->List[Order]:
        # return super().list_by_user(user_id, skip, limit)
        return (
            self.db.query(Order)
            .filter(Order.user_id==user_id)
            .order_by(Order.order_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )