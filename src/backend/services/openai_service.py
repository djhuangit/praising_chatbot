"""OpenAI API integration service"""
from openai import OpenAI
import logging
from typing import Tuple
from src.config import OPENAI_API_KEY, OPENAI_MODEL, SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API"""

    def __init__(self):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.system_prompt = SYSTEM_PROMPT

    def generate_response(self, user_message: str) -> Tuple[str, int]:
        """
        Generate a response using OpenAI API

        Args:
            user_message: The user's input message

        Returns:
            Tuple of (response_text, tokens_used)

        Raises:
            Exception: If API call fails
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )

            ai_response = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            logger.info(f"Generated response with {tokens_used} tokens")

            return ai_response, tokens_used

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
