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
        #buscar o crear carrito si no tiene
        # cart=self.cart_repo.get_by_user_id(user_id)
        # if not cart:
        #     cart=self.cart_repo.create_cart(user_id)
            
        cart=self.get_or_create_cart(user_id )    
        #validar variante y verificar stock     
        variant=self.variant_repo.get_by_id(variant_id)
        
        if not variant:
            raise ValueError(f"La variante del product no existe")
        
        if variant.stock_current<quantity:
            raise ValueError(f"Stock insuficiente. Disponible: {variant.stock_current}")
        
        existing_item=next((item for item in cart.items if item.variant_id==variant_id), None)
        total_quantity=quantity +(existing_item.quantity if existing_item else 0)
        
        # if existing_item:
            # total_quantity+=existing_item.quantity
            
        if variant.stock_current<total_quantity:
            raise ValueError(f"No puedes agregar más. Ya tienes {existing_item.quantity} y el stock total es {variant.stock_current}")

        return self.cart_repo.add_or_update_item(cart.id, variant_id, quantity)
            
        
    def update_item_quantity(self, user_id:int, variant_id:int, new_quantity:int)->Cart:
        
        if new_quantity<=0:
            return self.remove_item_from_cart(user_id, variant_id)
        
        variant=self.variant_repo.get_by_id(variant_id)
        
        if not variant or variant.stock_current<new_quantity:
            raise ValueError(f"Stock insuficiente para actualizar a {new_quantity}")
        # if variant.stock_current<new_quantity:
            # raise ValueError(f"Solo hay {variant.stock_current} unidades disponibles")
        
        # cart=self.cart_repo.get_by_user_id(user_id)
        cart=self.get_or_create_cart(user_id)
        return self.cart_repo.update_item_quantity(cart.id, variant_id, new_quantity)
    
    def remove_item_from_cart(self, user_id:int, variant_id:int)->Cart:
        # cart=self.cart_repo.get_by_user_id(user_id)
        
        cart=self.get_or_create_cart(user_id)
        self.cart_repo.remove_item(cart.id, variant_id)
        # return self.cart_repo.get_by_user_id(user_id)
        return self.get_or_create_cart(user_id)
    
    def clear_cart(self, user_id:int)->None:
        # cart=self.cart_repo.get_by_user_id(user_id)
        cart=self.get_or_create_cart(user_id)
        if cart:
            # raise ValueError("No se encontro un carrito para este usuario")
        
            self.cart_repo.clear_cart(cart.id)