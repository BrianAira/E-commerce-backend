# # app/api/dependencies.py

from fastapi import Depends
from requests import Session

from app.application.services.mercado_pago import MercadoPagoService
from app.core.database import get_db
from app.domain.ports.payment_repository import IPaymentRepository
from app.infrastructure.external_apis.mercadopago_repository import MercadoPagoRepository
from app.core.config import settings
from app.infrastructure.repositories.order import SQLOrderRepository
from app.infrastructure.repositories.variant_repository import SQLVariantRepository

def get_payment_repo() -> IPaymentRepository:
    return MercadoPagoRepository(
        access_token=settings.MP_ACCESS_TOKEN,
        webhook_url=settings.MP_WEBHOOK_URL
    )

def get_payment_service(db:Session=Depends(get_db)):
    payment_repo=MercadoPagoRepository(
        access_token=settings.MP_ACCESS_TOKEN,
        webhook_url=settings.MP_WEBHOOK_URL
    )
    
    return MercadoPagoService(
        payment_provider=payment_repo,
        order_repo=SQLOrderRepository(db),
        variant_repo=SQLVariantRepository(db)
    )
