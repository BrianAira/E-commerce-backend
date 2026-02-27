from typing import List, Optional
from sqlmodel import Session
from app.domain.models.image import Image
from app.domain.models.product import Product
from app.domain.models.variant import VariantProduct
from app.domain.ports.product_repository import IProductRepository
from app.domain.schemas.product import ProductCreate, ProductFilterParams, ProductUpdate
from app.domain.schemas.variant import VariantCreate


class SQLProductRepository(IProductRepository):
    def __init__(self, db:Session):
        self.db=db
        
    def create(self, data:ProductCreate)->Product:
        try:
            #Se crea el objeto principal y se exluyen otras tablas
            new_product=Product(**data.model_dump(exclude={"variants", "image_urls"}))
            self.db.add(new_product)
            
            # new_product=Product(
            #     name=data.name,
            #     description=data.description,
            #     gender=data.gender,
            #     price=data.price,
            #     category_id=data.category_id,
            #     sku_base=data.sku_base,
                
            # )
            # self.db.add(new_product)
            self.db.flush()#Genera el ID del producto sin cerrar la transaccion
            
            for v_data in data.variants:
                # new_variant=VariantProduct(
                #     product_id=new_product.id,
                #     color=v_data.color,
                #     talle=v_data.talle,
                #     sku=v_data.sku,
                #     stock_current=v_data.stock_current,
                #     stock_min=v_data.stock_min,
                #     price=v_data.price if v_data.price else 0
                #     )
                self.db.add(VariantProduct(product_id=new_product.id, **v_data.model_dump()))
                
                
            for url in data.image_urls:
                new_image=Image(
                    product_id=new_product.id,
                    url=str(url)
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
        if params.category_id:
            query=query.filter(Product.category==params.category)
        if params.price_min:
            query=query.filter(Product.price>=params.price_min)
        if params.price_max:
            query=query.filter(Product.price<=params.price_max)
        if params.search:
            query=query.filter(Product.name.contains(params.search))
        
        return query.all()  
        
    def update_variant_stock(self, variant_id:int, quantity:int)->bool:
        variant=self.db.query(VariantProduct).filter(VariantProduct.id==variant_id).first()
        if variant:
            variant.stock_current=quantity
            self.db.commit()
            return True
        return False
    
    def add_variant(self, product_id:int, variant_data:VariantCreate)->VariantProduct:
        product=self.get_by_id(product_id)
        if not product:
            raise ValueError("El product no existe")
        
        new_variant=VariantProduct(
            # product_id=product_id,
            **variant_data.model_dump()
        )
        
        self.db.add(new_variant)
        self.db.commit()
        self.db.refresh(new_variant)
        return new_variant
    
    
    
    def update_product(self, product_id:int, data:ProductUpdate)->Product:
        product=self.get_by_id(product_id)
        if not product:
            raise ValueError("Producto no encontrado")
         
        update_data=data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
            
        try:
            self.db.commit()
            self.db.refresh(product)
            return product
        except Exception as e:
            self.db.rollback()
            raise e
        
    def add_images(self, product_id:int, image_urls:List[str])->List[Image]:
        product=self.get_by_id(product_id)
        if not product:
            raise ValueError("Producto no encontrado")
        
        new_images=[]
        for url in image_urls:
            img=Image(product_id=product_id, url=url)
            self.db.add(img)
            new_images.append(img)
            
        self.db.commit()
        return new_images

        # return super().add_images(product_id, image_urls)
        
    def get_by_sku(self, sku:str)->Product:
        return self.db.query(Product).filter(Product.sku_base==sku).first()