# app/api/router/payment_router.py
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks, status
from sqlmodel import Session
from app.api.dependencies.dependencies import get_payment_repo, get_payment_service
from app.api.router.order_router import get_order_service
from app.application.services.mercado_pago import MercadoPagoService
from app.application.services.order import OrderService
from app.core.config import settings
from app.core.database import get_db
from app.domain.models.order import OrderStatus
from app.domain.ports.payment_repository import IPaymentRepository
from app.infrastructure.external_apis.mercadopago_repository import MercadoPagoRepository
from app.infrastructure.repositories.order import SQLOrderRepository
from app.infrastructure.repositories.variant_repository import SQLVariantRepository # Donde guardas tu MP_ACCESS_TOKEN y WEBHOOK_URL
import json


router = APIRouter(prefix="/payments", tags=["Payments"])

# @router.post("/checkout/{order_id}")
# def checkout(order_id: int, service: MercadoPagoService = Depends(get_payment_repo)):
#     """Genera el link de pago para una orden"""
#     url = service.start_checkout(order_id, settings.MP_WEBHOOK_URL)
#     return {"payment_url": url}

@router.post("/webhook")
async def mp_webhook(
    request: Request, 
    service: MercadoPagoService = Depends(get_payment_service)
    ):
    """Recibe la notificación de Mercado Pago"""
    # MP envía el ID del pago en los query params o en el body dependiendo de la versión
    params =dict(request.query_params)
    # body=await request.json()
    body={}
    try:
        body=await request.json()
    except:
        pass
    
    print("\n" + "="*50)
    print("🔔 ¡NUEVA NOTIFICACIÓN DE MERCADO PAGO!")
    print(f"QUERY PARAMS: {params}")
    print(f"BODY: {json.dumps(body, indent=2)}")
    print("="*50 + "\n")
    
    resource_id=None
    topic=None
    # Caso 1: Formato que recibiste en consola (Merchant Order en el Body)
    if body.get("type") == "topic_merchant_order_wh":
        resource_id = body.get("id")
        topic = "merchant_order"
    
    # Caso 2: Formato de Pago Directo en el Body
    elif body.get("type") == "payment":
        resource_id = body.get("data", {}).get("id")
        topic = "payment"
    
    # Caso 3: Formato por Query Params (Versiones antiguas o fallback)
    elif params.get("topic") or params.get("type"):
        topic = params.get("topic") or params.get("type")
        resource_id = params.get("id") or params.get("data.id")

    if resource_id and topic:
        print(f"🔎 Procesando {topic} ID: {resource_id}...")
        # Llamamos a la función inteligente del servicio
        success = service.process_notificaction(str(resource_id), topic)
        return {"status": "success" if success else "ignored"}
    
    # payment_id=None
    # if params.get("type")=="payment":
    #     payment_id=body.get("data", {}).get("id")
    # elif params.get("topic")=="payment":
    #     payment_id=params.get("id")
        
    # if payment_id:
    #     payment_id_str=str(payment_id)
    #     print(f"🔎 Procesando pago ID: {payment_id}...")
    #     success = service.process_payment_notification(payment_id_str)
        
    #     if success:
    #         print("✅ El proceso terminó con éxito")
    #     else:
    #         print("❌ El pago no fue aprobado o hubo un error")        
        
    #     return {"status":"success" if success else "ignored"}

    print("NO SE PUDO DETERMINAR EL ID O EL TIPO DE RECURSO")
    return {"status": "no_resource_id"}

@router.get("/success")
async def payment_success(
    payment_id:str,
    external_reference:str,
    status:str,
    service:MercadoPagoService=Depends(get_payment_service)
):
    print(f"Usuario regreo de MP. Procesando Pago:{payment_id} para Order: {external_reference}")
    
    success=service.process_payment_notification(payment_id)
    
    if success:
        return {
            "mensaje":"Pago verificado con exito",
            "order_id":external_reference,
            "nuevo_estado":"PAID"
        }
        
    raise HTTPException(status_code=400, detail="No se pudo verificar el pago")

@router.get("/failure")
async def payment_failure(
    external_reference: str, 
    preference_id: str,
    status: str = None
):
    print(f"❌ El pago para la orden {external_reference} falló o fue cancelado.")
    print(f"ID de preferencia: {preference_id}")
    
    # Aquí podrías, por ejemplo, marcar la orden como 'CANCELLED' si quisieras
    return {
        "status": "failure",
        "message": f"El pago de la orden {external_reference} no pudo ser procesado.",
        "sugerencia": "Intenta nuevamente desde el carrito."
    }