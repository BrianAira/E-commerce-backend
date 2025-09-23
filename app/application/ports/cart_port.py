from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.cart import Cart, CartCreate, CartUpdate


class ICartRepository(ABC):
    """Contrato para el repositorio de Carritos"""

    @abstractmethod
    def create(self, cart: CartCreate) -> Cart:
        """Crear un nuevo carrito"""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, cart_id: int) -> Optional[Cart]:
        """Obtener un carrito por su ID"""
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[Cart]:
        """Obtener el carrito de un usuario (1 a 1)"""
        raise NotImplementedError

    @abstractmethod
    def update(self, cart_id: int, cart_data: CartUpdate) -> Optional[Cart]:
        """Actualizar un carrito"""
        raise NotImplementedError

    @abstractmethod
    def delete(self, cart_id: int) -> bool:
        """Eliminar un carrito"""
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[Cart]:
        """Listar todos los carritos"""
        raise NotImplementedError
