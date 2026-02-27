
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ImageBase(BaseModel):
    
    
    url:str=Field(..., description="URl de la imagen")
    is_main:bool=Field(default=False, description="Imagen principal?")
    position:int=Field(default=0, description="Orden de presentacion en galeria")
    
    
class ImagenCreate(ImageBase):
    product_id:int
    
class ImageUpdate(BaseModel):
    is_main:Optional[bool]=None
    position:Optional[int]=None

class ImageResponse(ImageBase):
    id:int
    product_id:int
    
    model_config=ConfigDict(from_attributes=True)
    