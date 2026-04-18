
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.domain.schemas.image import ImageResponse
from app.domain.schemas.variant import VariantResponse


class ProductBase(BaseModel):
    name:str=Field(...,min_length=3, max_length=255)
    description:Optional[str]=Field(None, max_length=500)
    gender:str
    price:float=Field(..., gt=0)
    category_id:Optional[int]=None
    sku_base:str=Field(..., min_length=3, max_length=50)
    
class ProductCreate(ProductBase):
    # pass
    image_urls:Optional[List[str]]=[]
    variants:Optional[List[VariantResponse]]=[]

class ProductUpdate(BaseModel):
    name:Optional[str]=None
    price:Optional[float]=None
    description:Optional[str]=None
    category_id:Optional[int]=None
    sku_base:Optional[str]=None

class ProductResponse(ProductBase):
    id:int
    
    variants:List[VariantResponse]=[]
    images:List[ImageResponse]=[]
    
    model_config=ConfigDict(from_attributes=True)
    

class ProductFilterParams(BaseModel):
    category_id:Optional[int]=None
    price_min:Optional[float]=None
    price_max:Optional[float]=None
    search:Optional[str]=None
    order:Optional[str]="asc"
    
    
