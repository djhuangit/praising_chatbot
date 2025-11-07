"""Gradio chat interface component"""
import gradio as gr
import logging
from src.backend.services import OpenAIService, DemoOpenAIService, StatsService

logger = logging.getLogger(__name__)


def create_gradio_interface(
    openai_service: OpenAIService,
    stats_service: StatsService
) -> gr.Blocks:
    """
    Create Gradio chat interface

    Args:
        openai_service: OpenAI service instance (can be DemoOpenAIService or OpenAIService)
        stats_service: Stats service instance

    Returns:
        Gradio Blocks interface
    """

    # Check if demo mode is active
    is_demo_mode = isinstance(openai_service, DemoOpenAIService)

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
        # Demo mode banner (only shown if demo mode is active)
        if is_demo_mode:
            gr.Markdown(
                """
                <div style="background-color: #fff3cd; border: 2px solid #ffc107; border-radius: 8px; padding: 15px; margin-bottom: 20px;">
                    <h3 style="margin-top: 0; color: #856404;">⚠️ DEMO MODE ACTIVE</h3>
                    <p style="margin-bottom: 0; color: #856404;">
                        <strong>This application is running in demo mode.</strong><br>
                        Responses are generated from predefined templates - no OpenAI API calls are being made.<br>
                    </p>
                </div>
                """
            )

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

        # Footer with mode-specific information
        footer_text = "---\n💡 **About**: "
        if is_demo_mode:
            footer_text += "Running in **DEMO MODE** with mock responses. "
        else:
            footer_text += "This chatbot uses **GPT-4o-mini** to provide supportive and encouraging responses. "
        footer_text += "All statistics are tracked in-memory and reset when the server restarts."

        gr.Markdown(footer_text)

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
