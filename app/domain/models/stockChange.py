from pydantic import BaseModel, Field

class StockChange(BaseModel):
    delta:int=Field(gt=0, description="Cantidad a sumar al stock actual")
    
