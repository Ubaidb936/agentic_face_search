from abc import ABC, abstractmethod
from typing import Any

class BaseStorageService(ABC):
    @abstractmethod
    def upload_file(self, file_path: str) -> str:
        raise NotImplementedError("upload_file method must be implemented by subclasses")
    
    @abstractmethod
    def get_file_url(self, file_path: str) -> str:
        raise NotImplementedError("get_file_url method must be implemented by subclasses")  


class JsonStorage(ABC):
    @abstractmethod
    def put(self, table: str, value: dict) -> None:
        raise NotImplementedError("put method must be implemented by subclasses")
    def get(self, table: str, column_name: str, value: Any) -> Any:
        raise NotImplementedError("get method must be implemented by subclasses")