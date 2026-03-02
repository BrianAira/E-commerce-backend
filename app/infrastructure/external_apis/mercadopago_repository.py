from app.domain.models.order import Order
from app.domain.ports.payment_repository import IPaymentRepository
import mercadopago

class MercadoPagoRepository(IPaymentRepository):
    def __init__(self, access_token:str, webhook_url:str):
        self.sdk=mercadopago.SDK(access_token)
        self.webhook_url=webhook_url
        
    def create_payment_preference(self, order_data:Order)->str:
        base_url=self.webhook_url.rstrip("/")
        full_webhook_url=f"{base_url}/payments/webhook"
        print(f"url base: {base_url}")
        print(f"DEBUG: Registrando webhook en mp: {full_webhook_url}" )
        
        preference_data={
            "items":[    
                {
                    "title": f"Pedido Mayorista #{order_data.id}",
                    "quantity": 1,
                    "unit_price": round(float(order_data.total_amount),2),
                    "currency_id": "ARS"
                }
            ],
            "external_reference":str(order_data.id),
            "notification_url":full_webhook_url,
            "back_urls":{
                "success":f"{base_url}/payments/success",
                "failure":f"{base_url}/payments/failure",
                "pending":f"{base_url}/payments/pending"
            },
            "auto_return":"approved",
            "binary_mode":True
            
        }
        result=self.sdk.preference().create(preference_data)
        
        if result["status"]>=400:
            raise ValueError(f"Error al crear la preferencia en MercadoPago: {result["response"]}")
        return result["response"]["init_point"]
    
    def get_payment_details(self, payment_id:int)->dict:
        #usamos str para el payment id para envitar problemas de desbordamiento o tipos
        payment=self.sdk.payment().get(str(payment_id))
        
        if payment["status"]>=400:
            raise ValueError(f"Error al obtener detalles del pago: {payment["response"]}")
        
        response=payment["response"]
        return {
            # "status": payment["response"]["status"],
            "status":response.get("status"),
            # "order_id": payment["response"]["external_reference"]
            "order_id":response.get("external_reference"),
            "payment_id":response.get("id")
        }
        
    def get_merchant_order(self, merchant_id:str)->dict:
        order=self.sdk.merchant_order().get(str(merchant_id))
        if order["status"]>=400:
            raise ValueError(f"Error en merchant Order: {order["response"]}")
        
        return order["response"]
    
    
    