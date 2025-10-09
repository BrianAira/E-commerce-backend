from typing import List, Optional
from sqlmodel import Session, select
from app.domain.models.cart_item import CartItem, CartItemCreate, CartItemUpdate
from app.application.ports.cart_item_port import ICartItemRepository

class CartItemRepository(ICartItemRepository):
    def __init__(self, session:Session):
        self.session=session
        
    def create(self, item:CartItemCreate, cart_id:int, product_id:int)->CartItem:
        db_item=CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=item.quantity,
            subtotal=item.subtotal
        )
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item
    
    def get_by_id(self, item_id:int)->Optional[CartItem]:
        return self.session.get(CartItem, item_id)
    
    def list_by_cart_id(self, cart_id:int)->List[CartItem]:
        statement=select(CartItem).where(CartItem.cart_id==cart_id)
        return list(self.session.exec(statement))
    
    def update(self, item_id:int, item_data:CartItemUpdate)->Optional[CartItem]:
        db_item=self.session.get(CartItem, item_id)
        
        if not db_item:
            return None
        
        for key, value in item_data.dict(exclude_unset=True).items():
            setattr(db_item, key, value)
            
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item
    
    def delete(self, item_id:int)->bool:
        db_item=self.session.get(CartItem, item_id)
        if not db_item:
            return False
        
        self.session.delete(db_item)
        self.session.commit()
        return True