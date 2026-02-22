from abc import ABC, abstractmethod
from typing import Type, Any
from pydantic import BaseModel

class BaseLLLClient(ABC):
    @abstractmethod
    async def parse(
        self, 
        llm_input: list,
        response_format: Type[BaseModel],
        temperature: float = 0.1,
        ) -> Any:
        """
        Send messages to a model and return parsed structured output
        conforming to `response_format` (e.g., a Pydantic model).
        """
        ...

