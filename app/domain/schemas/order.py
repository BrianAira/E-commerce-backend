from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.domain.models.order import OrderStatus


class OrderItemResponse(BaseModel):
    id:int
    variant_id:int
    quantity:int
    unit_price:Decimal
    
    model_config=ConfigDict(from_attributes=True)
    
class OrderBase(BaseModel):
    status:OrderStatus=OrderStatus.PENDING   
    tracking_number:Optional[str]=None
    shipping_address_snapshot:str=Field(...,min_length=10, description="Direccion completa al momento de la compra"),
    
class OrderCreate(BaseModel):
    #Opcional si obtengo el carrito por el user_id del token
    cart_id:int
    shipping_address_id:int
    
class OrderUpdate(BaseModel):
    status:Optional[OrderStatus]=None
    tracking_number:Optional[str]=None
    
class OrderResponse(OrderBase):
    id:int
    user_id:int
    status:str
    order_date:datetime
    total_amount:Decimal
    
    
    items:List[OrderItemResponse]=[]
    
    model_config=ConfigDict(from_attributes=True) 
    
class OrderFilters(BaseModel):
    status:Optional[OrderStatus]=None
    location:Optional[str]=None
    postal_code:Optional[str]=None
    start_date:Optional[date]=None
    end_date:Optional[date]=None
    
class CheckoutResponse(BaseModel):
    # order:OrderResponse
    order_id:int
    total_amount:float
    status:str
    payment_url:str