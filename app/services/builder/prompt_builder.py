import logging

from app.prompts.transcript_qa import TRANSCRIPT_QA_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class PromptBuilder:

    def build(
            self,
            query: str,
            context: str,
            summary: str | None = None,
            message_history: str | None = None
    ) -> str:
        """
        Builds a prompt by combining the query and context.
        """
        try:

            logger.info("Building prompt for LLM.")

            messages = [
                {
                    "role": "system",
                    "content": self._build_system_prompt(),
                },
                {
                    "role": "user",
                    "content": self._build_user_prompt(
                        query=query,
                        context=context,
                        summary=summary,
                        message_history=message_history
                    ),
                },
            ]

            logger.info("Prompt built successfully.")

            return messages
        except Exception as e:
            logger.exception(f"Error building prompt for LLM: {e}")
            raise RuntimeError(f"Error building prompt for LLM: {e}")

    def _build_system_prompt(self) -> str:
        """
        Build the system prompt.
        """

        return TRANSCRIPT_QA_SYSTEM_PROMPT

    def _build_user_prompt(
        self,
        query: str,
        context: str,
        summary: str | None = None,
        message_history: str | None = None,
    ) -> str:
        """
        Build the user prompt.
        """
       
        summary = summary or "No previous conversation summary available."
        message_history = message_history or "No recent conversation history."

        return (
            "Conversation Summary:\n"
            "---------------------\n"
            f"{summary}\n\n"

            "Recent Conversation:\n"
            "---------------------\n"
            f"{message_history}\n\n"

            "Relevant Transcript Context:\n"
            "---------------------\n"
            f"{context}\n\n"

            "Current User Question:\n"
            "---------------------\n"
            f"{query}"
        )