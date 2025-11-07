"""Chat-related data models"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatMessage(BaseModel):
    """Model for a chat message"""
    content: str
    role: str = "user"
    timestamp: Optional[datetime] = None


class ChatResponse(BaseModel):
    """Model for chat response"""
    message: str
    tokens_used: int
    cost: float


class UsageStats(BaseModel):
    """Model for usage statistics"""
    total_tokens: int
    total_cost: float
    timestamp: datetime
