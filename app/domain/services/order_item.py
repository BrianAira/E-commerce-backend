from typing import List, Optional
from sqlmodel import Session
from decimal import Decimal

from app.domain.models.order_item import OrderItem, OrderItemRead, OrderItemCreate, OrderItemUpdate
from app.domain.models.order import Order, OrderUpdate

from app.application.ports.order_item_port import IOrderItemRepository
from app.application.ports.order_port import IOrderRepository
from app.application.ports.product_port import IProductRepository

class OrderItemService:
    def __init__(self, order_repo:IOrderRepository, order_item_repo:IOrderItemRepository, product_repo:IProductRepository, session:Session):
        self.order_repo=order_repo
        self.order_item_repo=order_item_repo
        self.product_repo=product_repo
        self.session=session
        
    def add_item(
        self,
        order_id:int, 
        product_id:int, 
        quantity:int,
        product_variant_id:Optional[int]=None
        )->OrderItemRead:
        #Validaciones
        if quantity <1:
            raise ValueError("La cantidad debe ser al menos 1")
        
        order=self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("Orden no encontrada")
        
        product=self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError("Producto no encontrado")
        
        if product.stock<quantity:
            raise ValueError("Stock insuficiente")
        
        #Calcular precio
        unit_price=product.sale_price
        subtotal=unit_price*Decimal(quantity)
        
        item_data=OrderItemCreate(
            order_id=order_id,
            product_id=product_id,
            product_variant_id=product_variant_id,
            quantity=quantity,
            subtotal=subtotal,
            unit_price=unit_price
        )
        
        item=self.order_item_repo.create(item_data)
        
        order.total_amount+=subtotal
        # self.order_repo.update(order_id, order)
        self.order_repo.update(order_id, OrderUpdate(total_amount=order.total_amount))
        
        product.stock-=quantity
        self.product_repo.update(product)
        
        return OrderItemRead.from_orm(item)
    
    def update_item_quantity(self, item_id:int, new_quantity:int)->OrderItemRead:
        item=self.order_item_repo.get_by_id(item_id)
        if not item:
            raise ValueError("Item no encontrado")
        
        product=self.product_repo.get_by_id(item.product_id)
        if not product:
            raise ValueError("Producto no encontrado")
        
        if new_quantity<1:
            raise ValueError("La cantidad debe ser al menos 1")
        
        delta=new_quantity- item.quantity
        if product.stock<delta:
            raise ValueError("stock insuficiente")
        
        #recalcular subtotal con el precio unitario original 
        new_subtotal=item.unit_price*Decimal(new_quantity)
        update_data=OrderItemUpdate(
            quantity=new_quantity, 
            unit_price=item.unit_price,
            subtotal=new_subtotal)
        
        updated_item=self.order_item_repo.update(item.id, update_data)
        
        order=self.order_repo.get_by_id(item.order_id)
        order.total_amount=sum(i.subtotal for i in order.items)
        self.order_repo.update(order.id, OrderUpdate(total_amount=order.total_amount))
        
        # product.stock-=delta
        
        
        
        # item.quantity=new_quantity
        # item.subtotal=product.sale_price*Decimal(new_quantity)
        
        # update_data=OrderItemUpdate(
        #     quantity=new_quantity,
        #     subtotal=product.sale_price * Decimal(new_quantity)
        # )
        # updated_item=self.order_repo_item.update(item.id, update_data)
        
        # order=self.order_repo.get_by_id(item.order_id)
        # order.total_amount=sum(i.subtotal for i in order.items)
        # order_update=OrderUpdate(total_amount=order.total_amount)
        # self.order_repo.update(order.id, order_update)
        
        product.stock-=delta
        self.product_repo.update(product)
        
        return OrderItemRead.from_orm(updated_item)
    
    def remove_item(self,item_id:int)->bool:
        item=self.order_item_repo.get_by_id(item_id)
        if not item:
            return False
        
        order=self.order_repo.get_by_id(item.order_id)
        product=self.product_repo.get_by_id(item.product_id)
        
        product.stock+=item.quantity
        self.product_repo.update(product)
        
        order.total_amount-=item.subtotal
        self.order_repo.update(order.id, OrderUpdate(total_amount=order.total_amount))
        # order_update=OrderUpdate(total_amount=order.total_amount)
        
        # self.order_repo.update(order.id, order_update)
        
        # product.stock+=item.stock
        # self.order_repo.update(order)
        
        # product.stock +=item.quantity
        # self.product_repo.update(product)
        
        return self.order_item_repo.delete(item_id)
    
    def list_items(self, order_id:int)->List[OrderItemRead]:
        items=self.order_item_repo.get_by_order(order_id)
        return [OrderItemRead.from_orm(i) for i in items]
    