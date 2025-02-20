from fastapi import FastAPI, HTTPException, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from openai import OpenAI
import os
from datetime import datetime
import uuid
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

# Configure OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found in environment variables")

app = FastAPI()

# Add this new root endpoint
@app.get("/")
async def read_root():
    return {"status": "ok", "message": "Praising Chat API is running"}

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://djpraisingchat.netlify.app", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

class ChatMessage(BaseModel):
    content: str

class ChatResponse(BaseModel):
    messages: List[dict]

# In-memory storage
chat_histories = {}  # session_id -> list of messages
total_cost = 0.0
total_tokens = 0

def calculate_cost(tokens_used: int) -> float:
    cost_per_million_tokens = 0.15  # Cost for gpt-4o-mini
    return (tokens_used / 1_000_000) * cost_per_million_tokens

@app.get("/api/chat/history")
async def get_chat_history(session_id: Optional[str] = Cookie(None)):
    if not session_id or session_id not in chat_histories:
        return {"messages": []}
    return {"messages": chat_histories[session_id]}

@app.post("/api/chat/message")
async def send_message(
    message: ChatMessage,
    session_id: Optional[str] = Cookie(None)
):
    global total_cost, total_tokens
    
    if not session_id:
        session_id = str(uuid.uuid4())
    
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    
    # Store user message
    user_message = {"role": "user", "content": message.content}
    chat_histories[session_id].append(user_message)

    # Generate AI response
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a supportive and encouraging friend. Your role is to provide positive, uplifting responses that make the user feel good about themselves and their achievements. Always maintain a positive, humorous and fluffy tone and keep the responses within 50 words. No emoji."},
                {"role": "user", "content": message.content}
            ]
        )
        ai_response = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        cost = calculate_cost(tokens_used)
        total_cost += cost
        total_tokens += tokens_used

        # Log token and cost details
        logging.info(f"Tokens used this request: {tokens_used}")
        logging.info(f"Cost incurred this request: ${cost:.5f}")
        logging.info(f"Total tokens used so far: {total_tokens}")
        logging.info(f"Total cost so far: ${total_cost:.5f}")
    except Exception as e:
        logging.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    # Store AI response
    ai_message = {"role": "assistant", "content": ai_response}
    chat_histories[session_id].append(ai_message)

    return {
        "messages": [user_message, ai_message],
        "session_id": session_id,
        "total_cost": total_cost
    }

@app.get("/api/chat/cost")
async def get_cost():
    return {"total_cost": total_cost}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 