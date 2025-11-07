"""
Praising Chatbot - Main entry point
A supportive and encouraging chat application
Built with FastAPI + Gradio for flexible deployment
"""
import logging
import gradio as gr
from src.backend.services import OpenAIService, StatsService
from src.backend.api import create_app
from src.frontend.components import create_gradio_interface
from src.config import HOST, PORT, LOG_LEVEL

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


def main():
    """Main application entry point"""
    logger.info("Starting Praising Chatbot application...")

    # Initialize services
    openai_service = OpenAIService()
    stats_service = StatsService()

    # Create FastAPI app
    app = create_app(stats_service)

    # Create Gradio interface
    demo = create_gradio_interface(openai_service, stats_service)

    # Mount Gradio on FastAPI
    app = gr.mount_gradio_app(app, demo, path="/gradio")

    logger.info(f"Application started on http://{HOST}:{PORT}")
    logger.info(f"Gradio UI available at http://{HOST}:{PORT}/gradio")
    logger.info(f"API docs available at http://{HOST}:{PORT}/docs")

    return app


if __name__ == "__main__":
    import uvicorn
    app = main()
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level=LOG_LEVEL.lower()
    )
