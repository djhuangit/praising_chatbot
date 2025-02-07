from sqlalchemy import Column, String, DateTime, Integer, Float
from database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String)  # "user" or "assistant"
    content = Column(String)
    timestamp = Column(DateTime)

class ChatHistory(Base):
    __tablename__ = "chat_histories"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime)

class CostTracking(Base):
    __tablename__ = "cost_tracking"

    id = Column(Integer, primary_key=True, index=True)
    total_cost = Column(Float, default=0.0)
    total_tokens = Column(Integer, default=0) 