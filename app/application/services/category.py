from app.domain.ports.category_repository import ICategoryRepository
from app.domain.schemas.category import CategoryCreate


class CategoryService:
    def __init__(self, category_repo:ICategoryRepository):
        self.category_repo=category_repo
        
    def create_category(self, data:CategoryCreate):
        return self.category_repo.create(data)
    
    def get_all_categories(self):
        return self.category_repo.list_all()
    
    def get_category_by_id(self, category_id:int):
        category=self.category_repo.get_by_id(category_id)
        if not category:
            raise ValueError("Categoria no encontrada")
        return category
    
    