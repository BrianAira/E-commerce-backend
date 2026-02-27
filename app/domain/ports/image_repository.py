from abc import ABC, abstractmethod


class IImageRepository(ABC):
    @abstractmethod
    def upload_file(self, file_content:bytes, filename:str, folder:str)->str:
        pass
    
    @abstractmethod
    def delete_file(self, file_url:str)->bool:
        pass
    