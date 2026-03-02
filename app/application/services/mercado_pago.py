from app.domain.ports.order_repository import IOrderRepository
from app.domain.ports.payment_repository import IPaymentRepository
from app.domain.ports.variant_repository import IVariantRepository
# import mercado_pago

class MercadoPagoService:
    def __init__(self, payment_provider:IPaymentRepository, order_repo:IOrderRepository, variant_repo:IVariantRepository):
        self.payment_provider=payment_provider
        self.order_repo=order_repo
        # self.variant_repo=variant_repo
        
    def start_checkout(self, order_id:int, webhook_url:str):
        order=self.order_repo.get_by_id(order_id)
        if not order: 
            raise ValueError("Order no encontrada")
        
        return self.payment_provider.create_payment_preference(order)
    
    def process_notificaction(self, resource_id:str, topic:str):
        print(f"DEBUG: Procesando notificación de tipo: {topic} para ID: {resource_id}")
        if topic == "payment":
            # Caso 1: Viene el ID del pago directamente
            return self.process_payment_notification(resource_id)

        elif topic in ["topic_merchant_order_wh", "merchant_order"]:
            # Caso 2: Viene una Merchant Order (Lo que te pasó en consola)
            # 1. Consultamos la "carpeta" completa
            merchant_order = self.payment_provider.get_merchant_order(resource_id)
            
            # 2. Buscamos si dentro hay pagos aprobados
            payments = merchant_order.get("payments", [])
            for p in payments:
                if p.get("status") == "approved":
                    # Si hay un pago aprobado, lo procesamos con la lógica de siempre
                    payment_id = str(p.get("id"))
                    return self.process_payment_notification(payment_id)
            
            print(f"INFO: Merchant Order {resource_id} recibida pero sin pagos aprobados aún.")
            return True # Respondemos 200 a MP para que no reintente
    
    def process_payment_notification(self, payment_id:str):
        payment_info=self.payment_provider.get_payment_details(payment_id)
        
        order_id=payment_info.get("order_id")
        #si es el pago de pryeba el order_id es nulo
        if not order_id:
            print(f"Notificacion recibida sin external_reference (pago de prueba id: {payment_id})")
            return True
        
        
        if payment_info["status"]=="approved":
            order=self.order_repo.get_by_id(int(order_id))
            if not order:
                print(f"❌ Orden {order_id} no encontrada en DB")
                return False
                
            if order.status == "PAID":
                print(f"✅ La orden {order_id} ya estaba marcada como pagada.")
                return True
                
            print(f"Pago aprobado para la orden {order_id}")
            # order_id=int(payment_info["order_id"])
            
            return self.order_repo.update_status(int(order_id), "PAID")
            # return True
        return False
