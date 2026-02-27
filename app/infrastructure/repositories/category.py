from typing import List, Optional

from sqlmodel import Session

from app.domain.models.category import Category
from app.domain.ports.category_repository import ICategoryRepository
from app.domain.schemas.category import CategoryCreate, CategoryUpdate


class SQLCategoryRepository(ICategoryRepository):
    def __init__(self, db:Session):
        self.db=db
        
    def get_by_id(self, category_id:int)->Optional[Category]:
        return self.db.query(Category).filter(Category.id==category_id).first()
    
    def list_all(self)->List[Category]:
        return self.db.query(Category).all()
    
    def create(self, data:CategoryCreate)->Category:
        new_category=Category(
            name=data.name,
            # description=data.description,
            slug=data.slug
            
        )
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category
    
    def delete(self, category_id:int)->bool:
        category=self.get_by_id(category_id)
        if category:
            self.db.delete(category)
            self.db.commit()
            return True
        return False
    
    def update(self, data:CategoryUpdate, category_id:int)->Category:
        category=self.get_by_id(category_id)
        if not category:
            raise ValueError("Categoria no encontrada")
        update_data=data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(category, key, value)
        try:
            self.db.commit()
            self.db.refresh(category)
            return category
        except Exception as e:
            self.db.rollback()
            raise e    
    