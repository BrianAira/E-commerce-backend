from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.application.services.category import CategoryService
from app.core.database import get_db
from app.domain.schemas.category import CategoryCreate, CategoryResponse
from app.infrastructure.repositories.category import SQLCategoryRepository


router=APIRouter(prefix="/categories", tags=["Categories"])

def get_category_service(db:Session=Depends(get_db)):
    repo=SQLCategoryRepository(db)
    return CategoryService(repo)

@router.get("/", response_model=List[CategoryResponse])
def list_categories(service:CategoryService=Depends(get_category_service)):
    return service.get_all_categories()

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(data:CategoryCreate, service: CategoryService=Depends(get_category_service)):
    return service.create_category(data)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id:int, service:CategoryService=Depends(get_category_service)):
    try:
        return service.get_category_by_id(category_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    