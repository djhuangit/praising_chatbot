# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "gradio>=4.44.0",
#     "openai>=1.61.1",
#     "python-dotenv>=1.0.0",
# ]
# ///

"""
Praising Chatbot - A supportive and encouraging chat application
Built with Gradio for simple deployment
"""

import gradio as gr
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

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

# In-memory cost tracking (resets on server restart)
total_cost = 0.0
total_tokens = 0

# System prompt for the chatbot
SYSTEM_PROMPT = """You are a supportive and encouraging friend. Your role is to provide positive,
uplifting responses that make the user feel good about themselves and their achievements.
Always maintain a positive, humorous and fluffy tone and keep the responses within 50 words. No emoji."""


def calculate_cost(tokens_used: int) -> float:
    """Calculate cost based on tokens used for gpt-4o-mini"""
    cost_per_million_tokens = 0.15
    return (tokens_used / 1_000_000) * cost_per_million_tokens


def chat(message: str, history: list) -> str:
    """
    Process chat message and return AI response

    Args:
        message: User's message
        history: Chat history in Gradio format [(user_msg, bot_msg), ...]

    Returns:
        AI response string
    """
    global total_cost, total_tokens

    try:
        # Generate AI response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
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

        return ai_response

    except Exception as e:
        logging.error(f"OpenAI API error: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"


def get_stats() -> str:
    """Get current usage statistics"""
    return f"Total Tokens: {total_tokens:,} | Total Cost: ${total_cost:.5f}"


def reset_stats():
    """Reset usage statistics"""
    global total_cost, total_tokens
    total_cost = 0.0
    total_tokens = 0
    return "Statistics reset successfully!"


# Create Gradio interface
with gr.Blocks(
    theme=gr.themes.Soft(),
    title="Praising Chatbot - Your Supportive Chat Space"
) as demo:
    gr.Markdown(
        """
        # 🌟 Praising Chatbot - Your Supportive Chat Space

        Welcome! I'm here to provide positive, uplifting responses to help you feel good
        about yourself and your achievements. Share anything with me!
        """
    )

    chatbot = gr.Chatbot(
        height=500,
        show_label=False,
        avatar_images=(None, None),
        bubble_full_width=False
    )

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Type your message here...",
            show_label=False,
            scale=4,
            container=False
        )
        send_btn = gr.Button("Send", variant="primary", scale=1)

    with gr.Row():
        clear_btn = gr.Button("Clear Chat")

    gr.Markdown("---")

    with gr.Accordion("📊 Usage Statistics", open=False):
        stats_display = gr.Textbox(
            value=get_stats(),
            label="Current Session Stats",
            interactive=False
        )
        with gr.Row():
            refresh_stats_btn = gr.Button("Refresh Stats", size="sm")
            reset_stats_btn = gr.Button("Reset Stats", size="sm", variant="stop")
        reset_message = gr.Textbox(visible=False)

    gr.Markdown(
        """
        ---
        💡 **About**: This chatbot uses GPT-4o-mini to provide supportive and encouraging responses.
        All statistics are tracked in-memory and reset when the server restarts.
        """
    )

    # Event handlers
    def respond(message, chat_history):
        bot_response = chat(message, chat_history)
        chat_history.append((message, bot_response))
        return "", chat_history, get_stats()

    def clear_chat():
        return None, get_stats()

    def handle_reset():
        msg = reset_stats()
        return msg, get_stats()

    # Wire up the events
    msg.submit(
        respond,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot, stats_display]
    )

    send_btn.click(
        respond,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot, stats_display]
    )

    clear_btn.click(
        clear_chat,
        outputs=[chatbot, stats_display]
    )

    refresh_stats_btn.click(
        get_stats,
        outputs=[stats_display]
    )

    reset_stats_btn.click(
        handle_reset,
        outputs=[reset_message, stats_display]
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
