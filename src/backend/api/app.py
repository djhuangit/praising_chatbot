"""FastAPI application factory"""
from fastapi import FastAPI
from src.config import APP_TITLE, APP_VERSION, APP_DESCRIPTION
from .routes import router, set_stats_service
from src.backend.services import StatsService


def create_app(stats_service: StatsService) -> FastAPI:
    """
    Create and configure FastAPI application

    Args:
        stats_service: Stats service instance to use

    Returns:
        Configured FastAPI app
    """
    app = FastAPI(
        title=APP_TITLE,
        description=APP_DESCRIPTION,
        version=APP_VERSION
    )

    # Set the stats service for routes
    set_stats_service(stats_service)

    # Include routes
    app.include_router(router)

    return app
