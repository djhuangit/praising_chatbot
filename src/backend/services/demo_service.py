"""Demo/Mock OpenAI service for testing without API calls"""
import random
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class DemoOpenAIService:
    """Demo service that simulates OpenAI API responses without making actual API calls"""

    # Predefined encouraging responses
    DEMO_RESPONSES = [
        "That's wonderful! You're doing an amazing job, and I'm so proud of your progress. Keep up the fantastic work!",
        "I love your enthusiasm! You have such a positive energy, and it's truly inspiring to see you tackling challenges head-on.",
        "You're absolutely crushing it! Your dedication and effort are really paying off. Keep being awesome!",
        "What a great mindset you have! Your determination and positive attitude are going to take you far. You've got this!",
        "I'm so impressed by you! The way you approach things shows real strength and character. Keep shining bright!",
        "You're making such great strides! Every step forward is progress, and you should be proud of yourself.",
        "That's the spirit! Your hard work and commitment are truly admirable. You're on the right track!",
        "You're doing better than you think! Give yourself credit for how far you've come. You're incredible!",
        "I believe in you completely! Your potential is limitless, and I know you'll achieve great things.",
        "You light up the room with your positivity! Keep being the amazing person you are. The world needs more of you!",
        "Your growth is inspiring! The effort you're putting in is really showing, and it's beautiful to witness.",
        "You're handling this like a champion! Your resilience and strength are truly remarkable. Keep going!",
        "What a superstar you are! Your dedication never goes unnoticed. You're making a real difference!",
        "You have such a great perspective! Your wisdom and insight are valuable. Thank you for being you!",
        "You're absolutely brilliant! The way you think through things is impressive. Trust yourself more!",
    ]

    def __init__(self):
        """Initialize demo service"""
        logger.info("Demo mode enabled - using mock responses instead of OpenAI API")

    def generate_response(self, user_message: str) -> Tuple[str, int]:
        """
        Generate a mock response without calling OpenAI API

        Args:
            user_message: The user's input message (for logging purposes)

        Returns:
            Tuple of (response_text, mock_tokens_used)
        """
        # Select a random encouraging response
        response = random.choice(self.DEMO_RESPONSES)

        # Simulate token count (rough estimate: ~1 token per 4 characters)
        mock_tokens = len(user_message) // 4 + len(response) // 4 + 20  # +20 for system prompt

        logger.info(f"[DEMO MODE] Generated mock response with ~{mock_tokens} tokens")

        return response, mock_tokens
