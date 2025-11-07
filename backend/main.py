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
from json_storage import storage

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
    allow_origins=["https://djpraisingchat.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    content: str

class ChatResponse(BaseModel):
    messages: List[dict]

# Cost tracking
total_cost = 0.0
total_tokens = 0

def calculate_cost(tokens_used: int) -> float:
    cost_per_million_tokens = 0.15  # Cost for gpt-4o-mini
    return (tokens_used / 1_000_000) * cost_per_million_tokens

@app.on_event("startup")
async def startup_event():
    global total_cost, total_tokens
    cost_data = await storage.get_cost_tracking()
    total_cost = cost_data.get("total_cost", 0.0)
    total_tokens = cost_data.get("total_tokens", 0)

@app.get("/api/chat/history")
async def get_chat_history(
    session_id: Optional[str] = Cookie(None)
):
    if not session_id:
        return {"messages": []}

    messages = await storage.get_chat_history(session_id)
    return {"messages": [{"role": msg["role"], "content": msg["content"]} for msg in messages]}

@app.post("/api/chat/message")
async def send_message(
    message: ChatMessage,
    session_id: Optional[str] = Cookie(None)
):
    global total_cost, total_tokens
    if not session_id:
        session_id = str(uuid.uuid4())

    # Store user message
    await storage.add_message(session_id, "user", message.content)

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

        # Update the cost and tokens in JSON storage
        await storage.update_cost_tracking(total_cost, total_tokens)

        # Log token and cost details
        logging.info(f"Tokens used this request: {tokens_used}")
        logging.info(f"Cost incurred this request: ${cost:.5f}")
        logging.info(f"Total tokens used so far: {total_tokens}")
        logging.info(f"Total cost so far: ${total_cost:.5f}")
    except Exception as e:
        logging.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    # Store AI response
    await storage.add_message(session_id, "assistant", ai_response)

    return {
        "messages": [
            {"role": "user", "content": message.content},
            {"role": "assistant", "content": ai_response}
        ],
        "session_id": session_id,
        "total_cost": total_cost
    }

@app.get("/api/chat/cost")
async def get_cost():
    return {"total_cost": total_cost}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 