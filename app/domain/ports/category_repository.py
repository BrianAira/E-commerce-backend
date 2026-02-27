from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.models.category import Category
from app.domain.schemas.category import CategoryCreate, CategoryUpdate


class ICategoryRepository(ABC):
    
    @abstractmethod
    def get_by_id(self, category_id:int)->Category:
        pass    
    
    @abstractmethod
    def get_by_slug(self, slug:str)->Optional[Category]:
        pass
    
    @abstractmethod
    def list_all(self)->List[Category]:
        pass
    
    @abstractmethod
    def create(self, data:CategoryCreate)->Category:
        pass
    
    @abstractmethod
    def update(self, data:CategoryUpdate)->Category:
        pass
    
    