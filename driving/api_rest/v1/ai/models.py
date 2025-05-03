from typing import List, Optional

from pydantic import BaseModel


class AIRequest(BaseModel):
    text: str
    context: Optional[str] = None
    system: Optional[str] = None
    session_id: Optional[str] = None  # Si no se proporciona, se generará uno nuevo


class AIResponse(BaseModel):
    content: str
    sources: List[str] = []
    session_id: str
