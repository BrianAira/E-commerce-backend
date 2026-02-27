from abc import ABC, abstractmethod
from typing import Optional

from app.domain.models.directions import Directions


class IDirectionRepository(ABC):
    @abstractmethod
    def get_by_id(self, direction_id:int)->Optional[Directions]:
        pass
    
    