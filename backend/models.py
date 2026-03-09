from typing import List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    text: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=4000)


class Citation(BaseModel):
    question: str
    score: int


class ChatResponse(BaseModel):
    response: str
    citations: List[Citation] = []
    used_rag: bool = False
    session_id: str


class HealthResponse(BaseModel):
    status: str
    model: Optional[str] = None
