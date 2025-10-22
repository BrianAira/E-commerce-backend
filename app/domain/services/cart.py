from typing import List, Optional
from sqlmodel import Session
from decimal import Decimal

from app.domain.models.cart import Cart, CartCreate, CartRead, CartUpdate
from app.domain.models.cart_item import CartItemRead, CartItemUpdate, CartItemCreate
from app.application.ports.cart_port import ICartRepository
from app.application.ports.user_port import IUserRepository
from app.application.ports.cart_item_port import ICartItemRepository
from app.application.ports.product_port import IProductRepository


class CartService:
    def __init__(self, cart_repo: ICartRepository, user_repo: IUserRepository, session: Session, cart_item_repo:ICartItemRepository, product_repo:IProductRepository):
        self.cart_repo = cart_repo
        self.user_repo = user_repo
        self.session = session
        self.cart_item_repo=cart_item_repo
        self.product_repo=product_repo

    def create_cart(self, cart_data: CartCreate) -> CartRead:
        user = self.user_repo.get_by_id(cart_data.user_id)
        if not user:
            raise ValueError("User does not exist")

        existing_cart = self.cart_repo.get_by_user_id(cart_data.user_id)
        if existing_cart:
            raise ValueError("User already has a cart")

        cart = self.cart_repo.create(cart_data)
        return CartRead.from_orm(cart)

    def get_cart(self, cart_id: int) -> Optional[CartRead]:
        cart = self.cart_repo.get_by_id(cart_id)
        return CartRead.from_orm(cart) if cart else None

    def get_cart_by_user(self, user_id: int) -> Optional[CartRead]:
        cart = self.cart_repo.get_by_user_id(user_id)
        return CartRead.from_orm(cart) if cart else None

    def update_cart(self, cart_id: int, update_data: CartUpdate) -> Optional[CartRead]:
        cart = self.cart_repo.update(cart_id, update_data)
        return CartRead.from_orm(cart) if cart else None
    
    # def clear_cart(self, cart_id:int)->Optional[CartRead]:
    #     cart=self.cart_repo.get_by_id(cart_id)
    #     if not cart:
    #         return None
    #     self.cart_item_repo.delete()
    
    def add_item(self, cart_id:int, item_data:CartItemCreate)->CartItemRead:
        cart=self.cart_repo.get_by_id(cart_id)
        if not cart:
            raise ValueError("Carrito no encontrado")
        product=self.product_repo.get_by_id(item_data.product_id)
        if not product:
            raise ValueError("Producto no encontrado")
        
        if product.stock<item_data.quantity:
            raise ValueError("Stock insuficiente")
        
        subtotal=product.sale_price*Decimal(item_data.quantity)
        
        
        # item_data.subtotal=product.sale_price *Decimal(item_data.quantity)
        # cart_item=self.cart_item_repo.create(item_data, cart_id)
        
        cart_item=self.cart_item_repo.create(
            CartItemCreate(
                cart_id=cart_id,
                product_id=product.id,
                quantity=item_data.quantity,
                subtotal=subtotal
            )
        )
        
        cart.total_amount=sum(i.subtotal for i in cart.items) + subtotal
        self.cart_repo.update(cart_id, CartUpdate(total_amount=cart.total_amount))
        
        product.stock-=item_data.quantity
        self.product_repo.update(product)
        
        return CartItemRead.from_orm(cart_item)
    
    def remove_item(self, item_id:int)->bool:
        item=self.cart_item_repo.get_by_id(item_id)
        if not item:
            raise ValueError("Item no encontrado")
        
        cart =self.cart_repo.get_by_id(item.cart_id)
        product=self.product_repo.get_by_id(item.product_id)
        
        cart.total_amount-=item.subtotal
        self.cart_repo.update(cart.id, CartUpdate(total_amount=cart.total_amount))
        
        product.stock+=item.quantity
        
        self.product_repo.update(product)
        
        return self.cart_item_repo.delete(item_id)

    def delete_cart(self, cart_id: int) -> bool:
        return self.cart_repo.delete(cart_id)

    def list_carts(self) -> List[CartRead]:
        carts = self.cart_repo.list_all()
        return [CartRead.from_orm(c) for c in carts]

    
    def update_item_quantity(self, item_id:int, new_quantity:int)->CartItemRead:
        item=self.cart_item_repo.get_by_id(item_id)
        if not item:
            raise ValueError("Item no encontrado")
        
        product=self.product_repo.get_by_id(item.product_id)
        if not product:
            raise ValueError("Producto no encontrado")
        
        if new_quantity<1:
            raise ValueError("La cantidad debe ser al menos 1")
        
        delta=new_quantity-item.quantity
        if delta>0 and product.stock<delta:
            raise ValueError("Stock insuficiente")
        
        new_subtotal=product.sale_price*Decimal(new_quantity)
        
        
        # item.quantity=new_quantity
        # item.subtotal=product.sale_price*Decimal(new_quantity)
        updated_item=self.cart_item_repo.update(item.id, CartItemUpdate(quantity=new_quantity, subtotal=new_subtotal))
        
        
        cart=self.cart_repo.get_by_id(item.cart_id)
        cart.total_amount=sum(i.subtotal for i in cart.items)
        self.cart_repo.update(cart.id, CartUpdate(total_amount=cart.total_amount))
        
        product.stock-=delta
        
        self.product_repo.update(product)
        
        return CartItemRead.from_orm(updated_item)
    
    def clear_cart(self, cart_id:int)->CartRead:
        cart=self.cart_repo.get_by_id(cart_id)
        if not cart:
            raise ValueError("Carrito no encontrado")
        
        for item in list(cart.items):
            product=self.product_repo.get_by_id(item.product_id)
            if product:
                product.stock+=item.quantity
                self.product_repo.update(product)
            self.cart_item_repo.delete(item.id)
        
        self.cart_repo.update(cart_id, CartUpdate(total_amount=Decimal("0")))
        cart.total_amount=Decimal("0")
        
        return CartRead.from_orm(cart)
    

    def list_items(self, cart_id:int)->List[CartItemRead]:
        items=self.cart_item_repo.list_by_cart_id(cart_id)
        return [CartItemRead.from_orm(i) for i in items]
    
    
    
    def _recaulculate_total(self, cart_id:int)->Decimal:
        cart=self.cart_repo.get_by_id(cart_id)
        total=sum(i.subtotal for i in cart.items)
        self.cart_repo.update(cart_id, CartUpdate(total_amount=total))
        return total