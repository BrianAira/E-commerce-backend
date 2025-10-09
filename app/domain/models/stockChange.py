from pydantic import BaseModel

class StockChange(BaseModel):
    delta:int
    
