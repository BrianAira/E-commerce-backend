# from app.infrastructure.repositories.cart_item import ICartItemRepository
# from app.infrastructure.repositories.cart import ICartRepository
# from app.infrastructure.repositories.product import IProductRepository
# from sqlmodel import Session
# from app.domain.models.cart_item import CartItemRead, CartItemUpdate, CartItemCreate
# from app.domain.models.cart import CartRead, CartUpdate, CartCreate
# from typing import List, Optional

# from decimal import Decimal

# class CartItemService:
#     def __init__(self, cart_item_repo:ICartItemRepository, cart_repo:ICartRepository, product_repo:IProductRepository, session:Session):
        
#         self.cart_item_repo=cart_item_repo
#         self.cart_repo=cart_repo
#         self.product_repo=product_repo
#         self.session=session
        
#     def add_item(self, cart_id:int, item_data:CartItemCreate)->CartItemRead:
#         cart=self.cart_repo.get_by_id(cart_id)
#         if not cart:
#             raise ValueError("Carrito no encontrado")
#         product=self.product_repo.get_by_id(item_data.product_id)
#         if not product:
#             raise ValueError("Producto no encontrado")
        
#         if product.stock<item_data.quantity:
#             raise ValueError("Stock insuficiente")
        
#         subtotal=product.sale_price*Decimal(item_data.quantity)
        
        
#         # item_data.subtotal=product.sale_price *Decimal(item_data.quantity)
#         # cart_item=self.cart_item_repo.create(item_data, cart_id)
        
#         cart_item=self.cart_item_repo.create(
#             CartItemUpdate(quantity=item_data.quantity, subtotal=subtotal),
#             cart_id,
#             product.id
#         )
        
#         cart.total_amount=sum(i.subtotal for i in cart.items) + subtotal
#         self.cart_repo.update(cart_id, CartUpdate(total_amount=cart.total_amount))
        
#         product.stock-=item_data.quantity
#         self.product_repo.update(product)
        
#         return CartItemRead.from_orm(cart_item)
    
#     def remove_item(self, item_id:int)->bool:
#         item=self.cart_item_repo.get_by_id(item_id)
#         if not item:
#             raise ValueError("Item no encontrado")
        
#         cart =self.cart_repo.get_by_id(item.cart_id)
#         product=self.product_repo.get_by_id(item.product_id)
        
#         cart.total_amount-=item.subtotal
#         self.cart_repo.update(cart.id, CartUpdate(total_amount=cart.total_amount))
        
#         product.stock+=item.quantity
        
#         self.product_repo.update(product)
        
#         return self.cart_item_repo.delete(item_id)

#     def update_item_quantity(self, item_id:int, new_quantity:int)->CartItemRead:
#         item=self.cart_item_repo.get_by_id(item_id)
#         if not item:
#             raise ValueError("Item no encontrado")
        
#         product=self.product_repo.get_by_id(item.product_id)
#         if not product:
#             raise ValueError("Producto no encontrado")
        
#         if new_quantity<1:
#             raise ValueError("La cantidad debe ser al menos 1")
        
#         delta=new_quantity-item.quantity
#         if product.stock<delta:
#             raise ValueError("Stock insuficiente")
        
#         new_subtotal=product.sale_price*Decimal(new_quantity)
        
        
#         # item.quantity=new_quantity
#         # item.subtotal=product.sale_price*Decimal(new_quantity)
#         updated_item=self.cart_item_repo.update(item.id, CartItemUpdate(quantity=new_quantity, subtotal=new_subtotal))
        
        
#         cart=self.cart_repo.get_by_id(item.cart_id)
#         cart.total_amount=sum(i.subtotal for i in cart.items)
#         self.cart_repo.update(cart.id, CartUpdate(total_amount=cart.total_amount))
        
#         product.stock-=delta
        
#         self.product_repo.update(product)
        
#         return CartItemRead.from_orm(updated_item)
    
#     def list_items(self, cart_id:int)->List[CartItemRead]:
#         items=self.cart_item_repo.list_by_cart_id(cart_id)
#         return [CartItemRead.from_orm(i) for i in items]