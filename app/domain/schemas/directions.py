from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class DirectionBase(BaseModel):
    street_address:str=Field(..., min_length=5, max_length=255 )
    city:str=Field(..., min_length=2, max_length=100)
    state:str=Field(..., min_length=2, max_length=100)
    postal_code:str=Field(..., min_length=4, max_length=20)
    country:str=Field(default="Argentina", max_length=100)
    additional_info:Optional[str]=Field(None, max_length=500)
    
class DirectionCreate(DirectionBase):
    #el usuario se puede obtener por el token de autenticacion
    #pero lo defino asi para la capa de servicio
    user_id:int
    
class DirectionUpdate(BaseModel):
    street_address:Optional[str]=None
    city:Optional[str]=None
    state:Optional[str]=None
    postal_code:Optional[str]=None
    country:Optional[str]=None
    additional_info:Optional[str]=None
    
class DirectionResponse(DirectionBase):
    id:int
    user_id:int
    
    model_config=ConfigDict(from_attributes=True)