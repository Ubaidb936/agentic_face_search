from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Image(BaseModel):
    id: int | None = None
    created_at: datetime | None = None
    user_id: str
    conversation: str
    photo_id: str