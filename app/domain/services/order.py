from typing import List, Optional
from decimal import Decimal
from sqlmodel import Session
from datetime import datetime, timezone

from app.domain.models.order import Order, OrderCreate, OrderRead, OrderUpdate
from app.domain.models.status_update import StatusUpdate

from app.application.ports.order_port import IOrderRepository
from app.application.ports.order_item_port import IOrderItemRepository


class OrderService:
    def __init__(self, order_repo:IOrderRepository, order_item_repo:IOrderItemRepository, session:Session):
        self.order_repo=order_repo
        self.order_item_repo=order_item_repo
        self.session=session
        # pass
        
    def create_order(self, order_data:OrderCreate)->OrderRead:
        if not order_data.status:
            raise ValueError("El estado de la orden no puede estar vacio")
        
        if order_data.total_amount is None or order_data.total_amount <Decimal("0"):
            raise ValueError("El monto total no puede ser negativo")
        
        order=self.order_repo.create(order_data)
        return OrderRead.from_orm(order)
    
    def get_order_by_id(self, order_id:int)->Optional[OrderRead]:
        order=self.order_repo.get_by_id(order_id)
        return OrderRead.from_orm(order) if order else None
    
    def list_orders(self)->List[OrderRead]:
        orders=self.order_repo.get_all()
        return [OrderRead.from_orm(o) for o in orders]
    
    def get_by_client(self, client_id:int)->List[OrderRead]:
        return self.get_by_client(client_id)
    
    def update_order(self, order_id:int, update_data:OrderUpdate)->Optional[OrderRead]:           
            
        updated=self.order_repo.update(order_id, update_data)
        return OrderRead.from_orm(updated) if updated else None
    
    def change_status(self, order_id:int, new_status:StatusUpdate)->OrderRead:
        order=self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("Orden no encontrada")
        # order.status=new_status
        update_data=OrderUpdate(status=new_status.new_status)
        
        updated=self.order_repo.update(order_id, update_data)
        return OrderRead.from_orm(updated)
    
    def add_item_to_order(self, order_id:int, product_id:int, quantity:int, subtotal:Decimal):
        order=self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("Orden no encontrada")
        
        item_data={
            "order_id":order_id,
            "product_id":product_id,
            "quantity":quantity,
            "subtotal":subtotal
        }
        
        item=self.order_item_repo.create(item_data)
        
        order.total_amount+=subtotal
        self.order_repo.update(order)
        
        return item
    
    def delete_order(self, order_id:int)->bool:
        order=self.order_repo.get_by_id(order_id)
        if not order:
            return False
        
        return self.order_repo.delete(order_id)
        