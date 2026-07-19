import logging

from groq import Groq
from app.core.config import settings
from app.services.retrieval.schemas import LLMResponse

logger = logging.getLogger(__name__)

class LLMService:

    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model_name = settings.LLM_MODEL

        if self.provider == "groq":
            self.client = Groq(
                api_key=settings.GROQ_API_KEY,
            )
        
        else:
            self.client = None

    def generate_response(
            self,
            messages: list[dict[str, str]],
    ) -> str:
        """
        Generates a response from the LLM based on the provided messages.
        """

        if self.provider == "groq":
            return self._generate_groq_response(messages)
        
        raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def _generate_groq_response(
            self,
            messages: list[dict[str, str]],
    ) -> str:
        """
        Generates a response from the Groq LLM based on the provided messages.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.2,
                max_tokens=1024,
            )

            logger.info("Response generated successfully from Groq LLM.")

            return LLMResponse(
                answer=response.choices[0].message.content,
                model=self.model_name,
            )
        
        except Exception as e:
            logger.exception(f"Error generating response from Groq LLM: {e}")
            raise RuntimeError(f"Error generating response from Groq LLM: {e}")