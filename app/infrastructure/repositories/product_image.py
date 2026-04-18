# from typing import List, Optional
# from sqlmodel import Session, select, update
# from sqlalchemy.exc import SQLAlchemyError

# from app.domain.models.image import ProductImage, ProductImageCreate
# from app.application.ports.product_image_port import IProductImageRepository


# class ProductImageRepository(IProductImageRepository):
#     def __init__(self, session: Session):
#         self.session = session

#     def create(self, image_data: ProductImageCreate) -> ProductImage:
#         image = ProductImage(**image_data.model_dump())
#         self.session.add(image)
#         self.session.commit()
#         self.session.refresh(image)
#         return image

#     def get_by_id(self, image_id: int) -> Optional[ProductImage]:
#         return self.session.get(ProductImage, image_id)

#     def list_by_product(self, product_id: int) -> List[ProductImage]:
#         statement = select(ProductImage).where(ProductImage.product_id == product_id)
#         return list(self.session.exec(statement))

#     def delete(self, image_id: int) -> bool:
#         image = self.session.get(ProductImage, image_id)
#         if not image:
#             return False
#         self.session.delete(image)
#         self.session.commit()
#         return True
    
#     def find_by_url(self, url: str, product_id: int) -> Optional[ProductImage]:
#         statement = select(ProductImage).where(
#             ProductImage.url == url,
#             ProductImage.product_id == product_id
#         )
#         return self.session.exec(statement).first()
    
#     def set_main_image(self, product_id: int, image_id: int) -> bool:
#         try:
#             # Desactivar todas las imágenes principales del producto
#             self.session.exec(
#                 update(ProductImage)
#                 .where(ProductImage.product_id == product_id)
#                 .values(is_main=False)
#             )

#             # Activar la nueva principal
#             result = self.session.exec(
#                 update(ProductImage)
#                 .where(
#                     ProductImage.id == image_id,
#                     ProductImage.product_id == product_id
#                 )
#                 .values(is_main=True)
#                 .returning(ProductImage.id)
#             ).first()

#             self.session.commit()
#             return bool(result)

#         except SQLAlchemyError:
#             self.session.rollback()
#             return False

