from abc import ABC, abstractmethod
from fastapi import UploadFile 

class BaseFaceSearchClient(ABC):
    @abstractmethod
    async def search(self, user_id: str, file: UploadFile ) -> list:
        """
        Search for similar faces in the database given an input image.
        """
        ...
        
    @abstractmethod    
    async def upload(self, user_id: str, file: UploadFile) -> None:
        """
        Upload a new face image along with its metadata to the database.
        """
        ...    