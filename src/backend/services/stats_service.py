"""Usage statistics tracking service"""
from datetime import datetime
from src.config import COST_PER_MILLION_TOKENS
from src.backend.models import UsageStats


class StatsService:
    """Service for tracking usage statistics"""

    def __init__(self):
        """Initialize stats tracking"""
        self.total_tokens = 0
        self.total_cost = 0.0

    def calculate_cost(self, tokens: int) -> float:
        """
        Calculate cost based on tokens used

        Args:
            tokens: Number of tokens used

        Returns:
            Cost in dollars
        """
        return (tokens / 1_000_000) * COST_PER_MILLION_TOKENS

    def add_usage(self, tokens: int) -> float:
        """
        Add token usage and return cost for this request

        Args:
            tokens: Number of tokens used

        Returns:
            Cost for this request
        """
        cost = self.calculate_cost(tokens)
        self.total_tokens += tokens
        self.total_cost += cost
        return cost

    def get_stats(self) -> UsageStats:
        """
        Get current usage statistics

        Returns:
            UsageStats object with current stats
        """
        return UsageStats(
            total_tokens=self.total_tokens,
            total_cost=round(self.total_cost, 5),
            timestamp=datetime.now()
        )

    def reset(self) -> None:
        """Reset all statistics to zero"""
        self.total_tokens = 0
        self.total_cost = 0.0

    def get_formatted_stats(self) -> str:
        """
        Get formatted statistics string

        Returns:
            Formatted string with token and cost info
        """
        return f"Total Tokens: {self.total_tokens:,} | Total Cost: ${self.total_cost:.5f}"
