"""Gradio chat interface component"""
import gradio as gr
import logging
from src.backend.services import OpenAIService, StatsService

logger = logging.getLogger(__name__)


def create_gradio_interface(
    openai_service: OpenAIService,
    stats_service: StatsService
) -> gr.Blocks:
    """
    Create Gradio chat interface

    Args:
        openai_service: OpenAI service instance
        stats_service: Stats service instance

    Returns:
        Gradio Blocks interface
    """

    def chat(message: str, history: list) -> str:
        """
        Process chat message and return AI response

        Args:
            message: User's message
            history: Chat history in Gradio format [(user_msg, bot_msg), ...]

        Returns:
            AI response string
        """
        try:
            # Generate AI response
            ai_response, tokens_used = openai_service.generate_response(message)

            # Track usage
            cost = stats_service.add_usage(tokens_used)

            # Log details
            logger.info(f"Tokens used this request: {tokens_used}")
            logger.info(f"Cost incurred this request: ${cost:.5f}")
            logger.info(f"Total tokens: {stats_service.total_tokens}")
            logger.info(f"Total cost: ${stats_service.total_cost:.5f}")

            return ai_response

        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"

    def get_stats() -> str:
        """Get current usage statistics"""
        return stats_service.get_formatted_stats()

    def reset_stats():
        """Reset usage statistics"""
        stats_service.reset()
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

    return demo
