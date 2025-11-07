import gradio as gr
from openai import OpenAI
import os
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db, init_db, async_session
from backend.models import Message, CostTracking
from dotenv import load_dotenv
from sqlalchemy.future import select
import logging
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Load environment variables
load_dotenv()

# Configure OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found in environment variables")

client = OpenAI(api_key=api_key)

# Cost tracking
total_cost = 0.0
total_tokens = 0

def calculate_cost(tokens_used: int) -> float:
    cost_per_million_tokens = 0.15  # Cost for gpt-4o-mini
    return (tokens_used / 1_000_000) * cost_per_million_tokens

# Load the initial cost from the database
async def load_initial_cost(db: AsyncSession) -> tuple[float, int]:
    result = await db.execute(select(CostTracking))
    cost_record = result.scalars().first()
    if cost_record:
        return cost_record.total_cost, cost_record.total_tokens
    else:
        # If no record exists, create one
        new_cost_record = CostTracking()
        db.add(new_cost_record)
        await db.commit()
        return 0.0, 0

# Initialize database and load cost
async def initialize():
    await init_db()
    async with async_session() as db:
        global total_cost, total_tokens
        total_cost, total_tokens = await load_initial_cost(db)
        logging.info(f"Initialized with total cost: ${total_cost:.5f}, total tokens: {total_tokens}")

# Load chat history for a session
async def load_chat_history(session_id: str):
    async with async_session() as db:
        result = await db.execute(
            select(Message).where(Message.session_id == session_id).order_by(Message.timestamp)
        )
        messages = result.scalars().all()
        return [[msg.content, None] if msg.role == "user" else [None, msg.content] for msg in messages]

# Chat function
async def chat(message: str, history: list, session_id: str):
    global total_cost, total_tokens

    if not message.strip():
        return history, f"💰 Total Cost: ${total_cost:.5f} | 🔢 Total Tokens: {total_tokens:,}"

    try:
        # Generate AI response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a supportive and encouraging friend. Your role is to provide positive, uplifting responses that make the user feel good about themselves and their achievements. Always maintain a positive, humorous and fluffy tone and keep the responses within 50 words. No emoji."},
                {"role": "user", "content": message}
            ]
        )
        ai_response = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        cost = calculate_cost(tokens_used)
        total_cost += cost
        total_tokens += tokens_used

        # Store messages in database
        async with async_session() as db:
            # Store user message
            user_message = Message(
                session_id=session_id,
                role="user",
                content=message,
                timestamp=datetime.utcnow()
            )
            db.add(user_message)

            # Store AI response
            ai_message = Message(
                session_id=session_id,
                role="assistant",
                content=ai_response,
                timestamp=datetime.utcnow()
            )
            db.add(ai_message)

            # Update cost tracking
            cost_record_result = await db.execute(select(CostTracking))
            cost_record = cost_record_result.scalars().first()
            if not cost_record:
                cost_record = CostTracking()
                db.add(cost_record)

            cost_record.total_cost = total_cost
            cost_record.total_tokens = total_tokens
            db.add(cost_record)
            await db.commit()

        # Log token and cost details
        logging.info(f"Tokens used this request: {tokens_used}")
        logging.info(f"Cost incurred this request: ${cost:.5f}")
        logging.info(f"Total tokens used so far: {total_tokens}")
        logging.info(f"Total cost so far: ${total_cost:.5f}")

        # Update chat history
        history.append([message, ai_response])
        cost_display = f"💰 Total Cost: ${total_cost:.5f} | 🔢 Total Tokens: {total_tokens:,}"

        return history, cost_display

    except Exception as e:
        logging.error(f"OpenAI API error: {str(e)}")
        error_msg = f"Error: {str(e)}"
        history.append([message, error_msg])
        return history, f"💰 Total Cost: ${total_cost:.5f} | 🔢 Total Tokens: {total_tokens:,}"

# Wrapper function to run async chat
def chat_wrapper(message, history, session_id):
    return asyncio.run(chat(message, history, session_id))

# Create Gradio interface
def create_interface():
    # Generate a unique session ID for this user
    session_id = str(uuid.uuid4())

    with gr.Blocks(title="KuaKua Qun - Praising Chatbot", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # 🌟 KuaKua Qun - Praising Chatbot
            ### Your supportive and encouraging AI friend!
            Ask me anything and I'll provide positive, uplifting responses to help you feel good about yourself.
            """
        )

        # Session ID (hidden)
        session_state = gr.State(session_id)

        # Cost display
        cost_display = gr.Textbox(
            label="Usage Statistics",
            value=f"💰 Total Cost: ${total_cost:.5f} | 🔢 Total Tokens: {total_tokens:,}",
            interactive=False,
            show_label=True
        )

        # Chatbot interface
        chatbot = gr.Chatbot(
            label="Chat History",
            height=500,
            show_label=True,
            avatar_images=(None, "🤗")
        )

        # Message input
        msg = gr.Textbox(
            label="Your message",
            placeholder="Type your message here and press Enter...",
            show_label=True,
            lines=2
        )

        # Buttons
        with gr.Row():
            submit = gr.Button("Send", variant="primary")
            clear = gr.Button("Clear Chat")

        # Event handlers
        msg.submit(
            chat_wrapper,
            inputs=[msg, chatbot, session_state],
            outputs=[chatbot, cost_display]
        ).then(
            lambda: "",
            outputs=[msg]
        )

        submit.click(
            chat_wrapper,
            inputs=[msg, chatbot, session_state],
            outputs=[chatbot, cost_display]
        ).then(
            lambda: "",
            outputs=[msg]
        )

        clear.click(
            lambda: ([], f"💰 Total Cost: ${total_cost:.5f} | 🔢 Total Tokens: {total_tokens:,}"),
            outputs=[chatbot, cost_display]
        )

        gr.Markdown(
            """
            ---
            **Note:** Each session has a unique ID. Your chat history is saved in the database.
            """
        )

    return demo

if __name__ == "__main__":
    # Initialize database and load cost
    asyncio.run(initialize())

    # Create and launch interface
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
