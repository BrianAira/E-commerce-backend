from typing import Optional
from sqlmodel import Session
from sqlalchemy.orm import joinedload
from app.domain.models.cart import Cart
from app.domain.models.cart_item import CartItem
from app.domain.models.variant import VariantProduct
from app.domain.ports.cart_repository import ICartRepository


class SQLCartRepository(ICartRepository):
    def __init__(self, db:Session):
        self.db=db
    #Metodo privado para no repetir logica de joinedload
    def _get_base_query(self):
        return self.db.query(Cart).options(
            joinedload(Cart.items)
            .joinedload(CartItem.variant)
            .joinedload(VariantProduct.product)
        )
        
        
    def get_by_id(self, cart_id:int)->Optional[Cart]:
        return self._get_base_query().filter(Cart.id==cart_id).first()
    
    
        # return self.db.query(Cart).options(
        #     joinedload(Cart.items)
        #     .joinedload(CartItem.variant)
        #     .joinedload(VariantProduct.product)
        # ).filter(Cart.id==cart_id).first
        
    def get_by_user_id(self, user_id:int)->Optional[Cart]:
        # return self.db.query(Cart).filter(Cart.user_id==user_id).first()
        return self._get_base_query().filter(Cart.id==user_id).first()
    
    def create_cart(self, user_id:int)->Cart:
        new_cart=Cart(user_id=user_id)
        self.db.add(new_cart)
        self.db.commit()
        self.db.refresh(new_cart)
        return self.get_by_id(new_cart.id)
    
    def add_or_update_item(self, cart_id:int, variant_id:int, quantity:int):
        item=self.db.query(CartItem).filter(
            CartItem.cart_id==cart_id,
            CartItem.variant_id==variant_id
        ).first()
        
        if item:
            item.quantity +=quantity
            
        else:
            new_item=CartItem(cart_id=cart_id, variant_id=variant_id, quantity=quantity)
            self.db.add(new_item)
            
            
        self.db.commit()
        return self.get_by_id(cart_id)
    
    def update_item_quantity(self, cart_id:int, variant_id:int, quantity:int)->Cart:
        item=self.db.query(CartItem).filter(
            CartItem.cart_id==cart_id,
            CartItem.variant_id==variant_id
        ).first()
        
        if item:
            item.quantity=quantity
            self.db.commit()
            
        return self.get_by_user_id(cart_id)
    
    def remove_item(self, cart_id:int, variant_id:int)->None:
        self.db.query(CartItem).filter(
            CartItem.cart_id==cart_id,
            CartItem.variant_id==variant_id
        ).delete()
        self.db.commit()
        
    def clear_cart(self, cart_id:int)->None:
        self.db.query(CartItem).filter(CartItem.cart_id==cart_id).delete()
        cart=self.db.query(Cart).filter(Cart.id==cart_id).first()
        if cart:
            cart.total_price=0
        
        self.db.commit()
        
    # def get_by_id(self, cart_id:int)->Optional[Cart]:
    #     return self.db.query(Cart).filter(Cart.id==cart_id).first()
    
    def update_cart_total(self, cart_id:int, new_total:float)->Cart:
        cart=self.get_by_id(cart_id)
        if cart:
            cart.total_price=new_total
            self.db.commit()
            self.db.refresh(cart)
        return cart