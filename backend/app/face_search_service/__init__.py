from fastapi import UploadFile
from app.face_search_service.base import BaseFaceSearchClient

class InHouseFaceSearchClient(BaseFaceSearchClient):
    async def search(self, user_id: str, file: UploadFile) -> list:
        # Implement your in-house face search logic here
        return []
    
    async def upload(self, user_id: str, file: UploadFile) -> None:
        # Implement your in-house face upload logic here
        pass    