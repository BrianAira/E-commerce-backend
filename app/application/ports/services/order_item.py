from typing import List, Optional
from sqlmodel import Session
from decimal import Decimal
from fastapi import HTTPException, status
from app.application.ports.product_variant_port import IProductVariantRepository
from app.domain.models.order_item import OrderItem, OrderItemRead, OrderItemCreate, OrderItemUpdate
from app.domain.models.order import Order, OrderUpdate

from app.application.ports.order_item_port import IOrderItemRepository
from app.application.ports.order_port import IOrderRepository
from app.application.ports.product_port import IProductRepository

class OrderItemService:
    def __init__(self, order_repo:IOrderRepository, order_item_repo:IOrderItemRepository, product_repo:IProductRepository, variant_repo:IProductVariantRepository, session:Session):
        self.order_repo=order_repo
        self.order_item_repo=order_item_repo
        self.product_repo=product_repo
        self.variant_repo=variant_repo
        self.session=session
        
    def add_item(
        self,
        order_id: int,
        product_id: int,
        quantity: int,
        product_variant_id: Optional[int] = None
    ) -> OrderItemRead:
        if quantity < 1:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La cantidad debe ser al menos 1")

        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Orden no encontrada")

        # Si hay variante → obtener desde ProductVariant
        if product_variant_id:
            variant = self.variant_repo.get_by_id(product_variant_id)
            if not variant:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Variante no encontrada")
            if variant.stock < quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Stock insuficiente para la variante seleccionada")

            unit_price = variant.price if hasattr(variant, "price") else variant.product.retail_price
            subtotal = unit_price * Decimal(quantity)
            variant.stock -= quantity
            self.variant_repo.update(variant.id, {"stock": variant.stock})
            product_id = variant.product_id  # asegura consistencia con producto base

        else:
            # Caso producto sin variantes
            product = self.product_repo.get_by_id(product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Producto no encontrado")
            if product.stock < quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Stock insuficiente")

            unit_price = product.retail_price
            subtotal = unit_price * Decimal(quantity)
            product.stock -= quantity
            self.product_repo.update(product)

        # Crear item
        item_data = OrderItemCreate(
            order_id=order_id,
            product_id=product_id,
            product_variant_id=product_variant_id,
            quantity=quantity,
            subtotal=subtotal,
            unit_price=unit_price
        )
        item = self.order_item_repo.create(item_data)

        # Actualizar total de la orden
        order.total_amount += subtotal
        self.order_repo.update(order_id, OrderUpdate(total_amount=order.total_amount))

        return OrderItemRead.from_orm(item)

    
    def update_item_quantity(self, item_id: int, new_quantity: int) -> OrderItemRead:
        item = self.order_item_repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Item no encontrado")

        if new_quantity < 1:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La cantidad debe ser al menos 1")

        delta = new_quantity - item.quantity

        # Verificar si el item tiene variante
        if item.product_variant_id:
            variant = self.variant_repo.get_by_id(item.product_variant_id)
            if not variant:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Variante no encontrada")
            if delta > 0 and variant.stock < delta:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Stock insuficiente")
            variant.stock -= delta
            self.variant_repo.update(variant.id, {"stock": variant.stock})
            unit_price = variant.price if hasattr(variant, "price") else variant.product.retail_price
        else:
            product = self.product_repo.get_by_id(item.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Producto no encontrado")
            if delta > 0 and product.stock < delta:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Stock insuficiente")
            product.stock -= delta
            self.product_repo.update(product)
            unit_price = product.retail_price

        new_subtotal = unit_price * Decimal(new_quantity)
        update_data = OrderItemUpdate(quantity=new_quantity, unit_price=unit_price, subtotal=new_subtotal)
        updated_item = self.order_item_repo.update(item.id, update_data)

        order = self.order_repo.get_by_id(item.order_id)
        order.total_amount = sum(i.subtotal for i in order.items)
        self.order_repo.update(order.id, OrderUpdate(total_amount=order.total_amount))

        return OrderItemRead.from_orm(updated_item)

    
    def remove_item(self, item_id: int) -> bool:
        item = self.order_item_repo.get_by_id(item_id)
        if not item:
            return False

        order = self.order_repo.get_by_id(item.order_id)

        if item.product_variant_id:
            variant = self.variant_repo.get_by_id(item.product_variant_id)
            if variant:
                variant.stock += item.quantity
                self.variant_repo.update(variant.id, {"stock": variant.stock})
        else:
            product = self.product_repo.get_by_id(item.product_id)
            if product:
                product.stock += item.quantity
                self.product_repo.update(product)

        order.total_amount -= item.subtotal
        self.order_repo.update(order.id, OrderUpdate(total_amount=order.total_amount))

        return self.order_item_repo.delete(item_id)

    
    def list_items(self, order_id:int)->List[OrderItemRead]:
        items=self.order_item_repo.get_by_order(order_id)
        return [OrderItemRead.from_orm(i) for i in items]
    