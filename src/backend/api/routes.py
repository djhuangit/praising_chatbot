"""API routes for the FastAPI backend"""
from fastapi import APIRouter
from datetime import datetime
from src.backend.services import StatsService

# Create router
router = APIRouter()

# Stats service will be injected
stats_service: StatsService = None


def set_stats_service(service: StatsService):
    """Set the stats service instance"""
    global stats_service
    stats_service = service


@router.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Praising Chatbot API",
        "version": "0.3.0",
        "endpoints": {
            "api_docs": "/docs",
            "chat_ui": "/gradio",
            "health": "/health",
            "stats": "/api/stats"
        }
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "praising-chatbot"
    }


@router.get("/api/stats")
async def get_stats():
    """Get current usage statistics via API"""
    if stats_service is None:
        return {"error": "Stats service not initialized"}

    stats = stats_service.get_stats()
    return {
        "total_tokens": stats.total_tokens,
        "total_cost": stats.total_cost,
        "timestamp": stats.timestamp.isoformat()
    }


@router.post("/api/stats/reset")
async def reset_stats():
    """Reset usage statistics via API"""
    if stats_service is None:
        return {"error": "Stats service not initialized"}

    stats_service.reset()
    return {
        "message": "Statistics reset successfully",
        "total_tokens": 0,
        "total_cost": 0.0
    }
