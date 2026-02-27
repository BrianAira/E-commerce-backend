from typing import List, Optional
from sqlmodel import Session
from app.domain.models.image import Image
from app.domain.models.product import Product
from app.domain.models.variant import VariantProduct
from app.domain.ports.product_repository import IProductRepository
from app.domain.schemas.product import ProductCreate, ProductFilterParams


class SQLProductRepository(IProductRepository):
    def __init__(self, db:Session):
        self.db=db
        
    def create(self, data:ProductCreate)->Product:
        try:
            new_product=Product(
                name=data.name,
                description=data.description,
                gender=data.gender,
                price=data.price,
                category_id=data.category_id,
                sku_base=data.sku_base,
                
            )
            self.db.add(new_product)
            self.db.flush()#Genera el ID del producto sin cerrar la transaccion
            
            for v_data in data.variants:
                new_variant=VariantProduct(
                    product_id=new_product.id,
                    color=v_data.color,
                    talle=v_data.talle,
                    sku=v_data.sku,
                    stock_current=v_data.stock_current,
                    stock_min=v_data.stock_min,
                    price=v_data.price if v_data.price else 0
                    )
                self.db.add(new_variant)
                
            for url in data.image_urls:
                new_image=Image(
                    product_id=new_product.id,
                    url=url
                )
                self.db.add(new_image)
                
                #confirmar todo en la base de datos
                self.db.commit()
                self.db.refresh(new_product)
                return new_product
        except Exception as e:
            self.db.rollback()#Si algo falla, deschace todo
            raise e
        
        
    def get_by_id(self, product_id:int)->Optional[Product]:
        return self.db.query(Product).filter(Product.id==product_id).first()
    
    def list_filtered(self, params:ProductFilterParams)->List[Product]:
        query=self.db.query(Product)
        
        # if params
        if params.category.id:
            query=query.filter(Product.category==params.category)
        if params.price_min:
            query=query.filter(Product.price>=params.price_min)
        if params.price_max:
            query=query.filter(Product.price<=params.price_max)
        if params.search:
            query=query.filter(Product.name.contains(params.search))
        
        return query.all()  
        
    