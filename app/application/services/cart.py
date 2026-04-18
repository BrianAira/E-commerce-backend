from app.domain.models.cart import Cart
from app.domain.ports.cart_repository import ICartRepository
from app.domain.ports.variant_repository import IVariantRepository

 
class CartService:
    def __init__(
        self, 
        cart_repo:ICartRepository,
        variant_repo:IVariantRepository
        
    ): 
        self.cart_repo=cart_repo
        self.variant_repo=variant_repo
        
    def _refresh_total(self, cart_id:int)->Cart:
        cart=self.cart_repo.get_by_id(cart_id)
        if not cart:
            return None
        
        new_total=sum(
            item.quantity*item.variant.product.price 
            for item in cart.items
            if item.variant and item.variant.product
        )
        
        return self.cart_repo.update_cart_total(cart_id, new_total)
        
    def get_or_create_cart(self, user_id:int)->Cart:
        cart=self.cart_repo.get_by_user_id(user_id)
        if not cart:
            cart=self.cart_repo.create_cart(user_id)
        return cart
        
    def get_user_cart(self, user_id:int)->Cart:
        cart=self.cart_repo.get_by_user_id(user_id)
        if not cart:
            return self.cart_repo.create_cart(user_id)
        return cart 
    
    def add_product_to_cart(self, user_id:int, variant_id:int, quantity:int)->Cart:
            
        cart=self.get_or_create_cart(user_id )    
        #validar variante y verificar stock     
        variant=self.variant_repo.get_by_id(variant_id)
        
        if not variant:
            raise ValueError(f"La variante del product no existe")
        
        existing_item=next((item for item in cart.items if item.variant_id==variant_id), None)
        total_quantity=quantity +(existing_item.quantity if existing_item else 0) 
               
        if variant.stock_current<quantity:
            raise ValueError(f"Stock insuficiente. Tienes {existing_item.quantity if existing_item else 0}, "
                             f"quieres sumar {quantity}, pero solo hay {variant.stock_current} en total.")
        
        if variant.stock_current<total_quantity:
            raise ValueError(f"No puedes agregar más. Ya tienes {existing_item.quantity} y el stock total es {variant.stock_current}")

        self.cart_repo.add_or_update_item(cart.id, variant_id, quantity)
        return self._refresh_total(cart.id)    
        
    def update_item_quantity(self, user_id:int, variant_id:int, new_quantity:int)->Cart:
        
        if new_quantity<=0:
            return self.remove_item_from_cart(user_id, variant_id)
        
        variant=self.variant_repo.get_by_id(variant_id)
        
        if not variant or variant.stock_current<new_quantity:
            raise ValueError(f"Stock insuficiente para actualizar a {new_quantity}")

        cart=self.get_or_create_cart(user_id)
        self.cart_repo.update_item_quantity(cart.id, variant_id, new_quantity)
        return self._refresh_total(cart.id)
    
    def remove_item_from_cart(self, user_id:int, variant_id:int)->Cart:

        
        cart=self.get_or_create_cart(user_id)
        self.cart_repo.remove_item(cart.id, variant_id)

        return self._refresh_total(cart.id)
    
    def clear_cart(self, user_id:int)->None:

        cart=self.get_or_create_cart(user_id)
        if cart:

        
            self.cart_repo.clear_cart(cart.id)
         