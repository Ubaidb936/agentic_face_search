import openai
from fastapi import HTTPException
from typing import Type, Any
import logging

from app.llm_service.base import BaseLLLClient
from app.utils.config import settings


logger = logging.getLogger(__name__)

class OpenAIClient(BaseLLLClient):
    """Implementation of BaseLLMClient that uses OpenAI's API."""
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def parse(
            self,
            llm_input: list,
            response_format: Type,
            temperature: float = 0.1,
    ) ->  Any:
        """
          Sends structured input to OpenAI and returns parsed output
          based on the given Pydantic model (response_format).
        """
        try:
            response = await self.client.responses.parse(
                model="gpt-4.1",
                input=llm_input,
                temperature=temperature,
                text_format=response_format,
            )
            return response.output[0].content[0].parsed
        except Exception as e:
           logger.exception("LLM call failed", e)
           raise HTTPException(
                 status_code=502,
                 detail="LLM service failed to produce a valid response",
            )
           
openai_client = OpenAIClient()


    
          



