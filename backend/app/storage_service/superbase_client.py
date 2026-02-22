import logging
from pathlib import Path
from fastapi import UploadFile
from supabase import create_client, Client
from typing import Any

from app.storage_service.base import BaseStorageService, JsonStorage
from app.utils.config import settings

logger = logging.getLogger(__name__)

class StorageError(Exception):
    """Base storage error"""

class StorageObjectNotFound(StorageError):
    pass

class StorageUnexpectedError(StorageError):
    pass

class ResourceAlreadyExistError(StorageError):
    pass

class SuperBaseClient(BaseStorageService, JsonStorage):
    def __init__(self):
        self.superbase_client: Client = create_client(settings.SUPER_BASE_PROJECT_URL, settings.SUPER_BASE_API_KEY)

    def upload_file(self, table: str, file_bytes: bytes, file_path: str) -> Any:
        try:
            response = self.superbase_client.storage.from_(table).upload(file_path, file_bytes, {"upsert": "true"})
            return response
        except Exception as e:
            if "resource already exists" in str(e):
                raise ResourceAlreadyExistError(f"File already exists: {file_path}")
            else:
                raise StorageUnexpectedError(f"Unexpected error: {str(e)}")
    
    def get_file_url(self, table: str, file_path) -> str:
        try:
            signed = (
                self.superbase_client
                    .storage
                    .from_(table)
                    .create_signed_url(file_path, expires_in=3600)
            )
            return signed
        except Exception as e:
            if "object not found" in str(e).lower():
                raise StorageObjectNotFound(f"File not found: {file_path}")
            else:
                raise StorageUnexpectedError(f"Unexpected error: {str(e)}")
    
    def put(self, table: str, value: dict) -> None:
        response = self.superbase_client.from_(table).insert(value).execute()
        return response

    def get(self, table: str, column_name: str,  value: Any, column_name1: str, value1: Any) -> Any:
        response = (
            self.superbase_client.from_(table)
            .select("*")
            .eq(column_name, value)
            .eq(column_name1, value1)
            .execute()
        )
        return response   
    
    def update(self, table: str, key: str, value: Any) -> None:
        response = (
            self.superbase_client.from_(table)
            .update({"name": "Earth"})
            .eq("id", 1)
            .execute()
        )        
        
superbase_client = SuperBaseClient()
# print(superbase_client.get_file_url("ubaid/10.jpe"))
# superbase_client.upload_file("ubaid/5.jpeg")
# superbase_client.put("planets", {"id": 1, "name": "Pluto"})
# print(superbase_client.get("planets"))
#  self.superbase_client.from_("planets")
#             .insert({"id": 1, "name": "Pluto"})
#             .execute()
# print(superbase_client.update("planets", {"id": 1, "name": "Earth"}))

# print(superbase_client.put("planets", {"id": 1, "name": "Saturn"}))


# self.superbase_client.from_("planets")
#             .select("*")
#             .eq("id", 1)
#             .execute()
# print(superbase_client.get("planets", "name", "Pluto"))



