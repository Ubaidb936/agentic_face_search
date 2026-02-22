import httpx
from fastapi import UploadFile
from app.face_search_service.base import BaseFaceSearchClient

local = "http://0.0.0.0:8000"
cloud = "http://18.191.190.96:8000"

class InHouseFaceSearchClient(BaseFaceSearchClient):
    def __init__(self):   
        self.httpx_client = httpx.AsyncClient(timeout=60, base_url=cloud, headers={"api-key": "12345"})
        pass
    
    async def search(self, user_id: str, file: UploadFile) -> list:
        response = await self.httpx_client.post(
            "/search",
            params={"user_id": user_id},
            files={"file": (file.filename, file.file, file.content_type)}
        ) 
        return response.json()
    
    async def upload(self, user_id: str, file: UploadFile) -> None:
        response = await self.httpx_client.post(
            "/upload",
            params={"user_id": user_id},
            files={"file": (file.filename, file.file, file.content_type)}
        )    

inhouse_face_search_client = InHouseFaceSearchClient()