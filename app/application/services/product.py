from typing import List, Optional
from app.domain.models.product import Product
from app.domain.models.variant import VariantProduct
from app.domain.ports.category_repository import ICategoryRepository
from app.domain.ports.image_repository import IImageRepository
from app.domain.ports.product_repository import IProductRepository
from app.domain.ports.variant_repository import IVariantRepository
from app.domain.schemas.product import ProductFilterParams, ProductUpdate
from app.domain.schemas.variant import VariantCreate, VariantUpdate
from app.domain.schemas.product import ProductCreate


class ProductService:
    def __init__(
        self,
        product_repo:IProductRepository,
        variant_repo:IVariantRepository,
        category_repo:ICategoryRepository,
        # image_repo:IImageRepository
    ):
        self.product_repo=product_repo
        self.variant_repo=variant_repo
        self.category_repo=category_repo
        # self.image_repo=image_repo

    def create_product(self, data:ProductCreate)->Product:
        category=self.category_repo.get_by_id(data.category_id)
        if not category:
            raise ValueError("La categoria especificada no existe")
        
        sku_exist=self.product_repo.get_by_sku(data.sku_base)
        if sku_exist:
            raise ValueError("SKu ya existente")
        # 2. Validación opcional: ¿El SKU base ya existe? 
    # (Podrías agregar un método get_by_sku_base en tu repo para esto)

    # 3. Como data ya trae la lista 'image_urls' desde el JSON, 
    # no necesitamos procesar archivos ni llamar a self.image_repo.upload_file.

    # 4. Delegamos la creación atómica al repositorio
        return self.product_repo.create(data)

    #Crear producto y cargar imagenes desde el dispositivo    
    # def create_product(self, data:ProductCreate, image_files:List[bytes])->Product:
    #     category=self.category_repo.get_by_id(data.category_id) 
    #     if not category:
    #         raise ValueError("La categoria especificada no existe")
          
    #     image_urls=[]
        
    #     for file in image_files:
    #         url=self.image_repo.upload_file(file, folder="products")
    #         image_urls.append(url)
            
    #     data.image_urls=image_urls
        
    #     return self.product_repo.create(data)
    
    def get_product_details(self, product_id:int)->Optional[Product]:
        product=self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError("Product no encontrad")
        return product
    
    def update_stock_by_sku(self, sku:str, new_quantity:int)->bool:
        """Logica para actualizar stock usando sku de variante"""   
        
        variant=self.variant_repo.get_by_sku(sku)
        if not variant:
            raise ValueError(f"No se encontro ninguna variante con el sku: {sku}")
        
        # return self.product_repo.update_variant_stock(variant.id, new_quantity)
        return self.variant_repo.update_stock(variant.id, new_quantity)
    
    def search_products(self, params:ProductFilterParams)->List[Product]:
        return self.product_repo.list_filtered(params)
    
    
    # Ajustado para recibir una sola variante como pide tu Router
    def add_new_variant(self, product_id: int, v_data: VariantCreate) -> VariantProduct:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError("Producto inexistente")
        
        existing = self.variant_repo.get_by_sku(v_data.sku)
        if existing:
            raise ValueError(f"El SKU {v_data.sku} ya existe")
            
        return self.product_repo.add_variant(product_id, v_data)
    
    # def add_variants_to_product(self, product_id:int, variants_data:VariantCreate)->VariantProduct:
    #     product=self.product_repo.get_by_id(product_id)
        
    #     if not product:
    #         raise ValueError("No se puede agregar variantes a un producto inexistente")
        
        # for v_data in variants_data:
        #     existing= self.variant_repo.get_by_sku(v_data.sku)
        #     if existing:
        #         raise ValueError(f"El sku {v_data.sku} ya esta en uso por otra variante o producto")
            
        #     #Aseguramos que el id sea el correcto
        #     v_data.product_id=product_id
            
        return self.variant_repo.create_many(variants_data)
    
    def update_variant_details(self, variant_id:int, data:VariantUpdate)->VariantProduct:
              
        variant=self.variant_repo.get_by_id(variant_id)
        if not variant:
            raise ValueError("Variante no encontrada")
        
        return self.variant_repo.update(variant_id, data)
    
    def update_product(self, product_id:int, data:ProductUpdate):
        return self.product_repo.update_product(product_id, data)
    
    def add_product_images(self, product_id:int, urls:List[str]):
        if not urls:
            raise ValueError("La lista de urls no puede estar vacia")
        
        return self.product_repo.add_images(product_id, urls)
    
    def add_stock_to_variant(self, variant_id:int, quantity:int):
        return self.variant_repo.update_stock(variant_id, quantity)
    
    def get_inventory_status_report(self):
        variants=self.variant_repo.get_all_variants_with_products()
        report=[]
        
        for v in variants:
            if v.stock_current<=0:
                status="AGOTADO"
            elif v.stock_current<=v.stock_min:
                status="ALERTA"
            else:
                status="NORMAL"
                
            report.append({
                "variant_id":v.id,
                "product_name": v.product.name,
                "sku":v.sku,
                "color":v.color,
                "talle":v.talle,
                "stock_current":v.stock_current,
                "status":status
            })
            
        return report
    