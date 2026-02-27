from app.domain.models.order import Order, OrderStatus
from app.domain.ports.cart_repository import ICartRepository
from app.domain.ports.order_repository import IOrderRepository
from app.domain.ports.payment_repository import IPaymentRepository
from app.domain.ports.product_repository import IProductRepository
from app.domain.ports.user_repository import IUserRepository
from app.domain.ports.variant_repository import IVariantRepository
from app.domain.schemas.order import OrderFilters


class OrderService:
    def __init__(
        self, 
        order_repo:IOrderRepository,
        cart_repo:ICartRepository,
        variant_repo:IVariantRepository,
        user_repo:IUserRepository,
        product_repo:IProductRepository,
        payment_repo:IPaymentRepository
    ):
        self.order_repo=order_repo
        self.cart_repo=cart_repo
        self.variant_repo=variant_repo
        self.user_repo=user_repo
        self.product_repo=product_repo
        self.payment_repo=payment_repo
        
    def checkout(self, user_id:int, direction_id:int)->Order:
        
        #obtener carrito y validar que no este vacio
        cart=self.cart_repo.get_by_user_id(user_id)
        if not cart or not cart.items:
            raise ValueError("El carrito esta vacio")
        
        #validar que la direccion pertenezca al usuario
        user_addresses=self.user_repo.get_addresses(user_id)
        if not any(addr.id== direction_id for addr in user_addresses):
            raise ValueError("Direccion de envio invalida")
        
        direction_obj=self.user_repo.get_address_by_id(direction_id)
        
        direction_txt= f"{direction_obj.street_address} {direction_obj.city}, {direction_obj.country}, {direction_obj.postal_code}"        
        #validacion de stock y calculo total
        total_amount=0
        order_items_data=[]
        
              
        for item in cart.items:
            variant=self.variant_repo.get_by_id(item.variant_id)     
            
            if not variant:
                raise ValueError(f"La variante {item.variant_id} no existe")
                   
            if variant.stock_current<item.quantity:
                raise ValueError(f"Stock insuficiente para {variant.sku} dispoinible: {variant.stock_current}")
            
            #logica de precio
            product=self.product_repo.get_by_id(variant.product_id)
            
            unit_price=variant.price if variant.price>0 else product.price
            
            # subtotal=product.price
            total_amount+=unit_price*item.quantity
            
            order_items_data.append({
                "variant_id":variant.id,
                "quantity":item.quantity,
                "unit_price":unit_price
            })
            
            #Crear la orden
            #order repo maneja la creacion de orden y sus items
  
        new_order=self.order_repo.create(
            user_id=user_id,
            total_amount=total_amount,
            shipping_address_snapshot=direction_txt,
            items=order_items_data
        )
            
            #Actualizar stock y vaciar carrito
        for item in cart.items:
            self.variant_repo.reduce_stock(item.variant_id, item.quantity)
        
        payment_url=self.payment_repo.create_payment_preference(new_order)
                
        self.cart_repo.clear_cart(cart.id)
        
        
        
        
            
        return {
            "order":new_order,
            "payment_url":payment_url
            # new_order
            }
        
    def cancel_order(self, order_id:int):
        
        order=self.order_repo.get_by_id(order_id)
        if order.status==OrderStatus.CANCELLED:
            raise ValueError("La orden ya esta cancelada")
        
        for item in order.items:
            self.variant_repo.increase_stock(item.variant_id, item.quantity)
            
        return self.order_repo.update_status(order_id, OrderStatus.CANCELLED)
    
    
    def get_order_by_id(self, order_id:int):
        return self.order_repo.get_by_id(order_id)
    
    def get_orders_by_user_id(self, user_id:int):
        return self.order_repo.get_orders_by_user_id(user_id)
    
    
    
    def get_all(self, filters:OrderFilters):
        return self.order_repo.get_all_orders(filters)
    
    def update_order_status(self, order_id:int, new_status:OrderStatus)->Order:
        order=self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"No se encontro la orden con id: {order_id}")
        
        if order.status==OrderStatus.DELIVERED and new_status==OrderStatus.CANCELLED:
            raise ValueError("No se puede cancelar una orden que ya ha sido entregada")
        
        update_order=self.order_repo.update_status(order_id, new_status)
        
        return update_order
    
    