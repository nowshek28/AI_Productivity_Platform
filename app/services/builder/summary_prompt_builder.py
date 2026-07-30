import logging

from app.prompts.chat_summary import CHAT_SUMMARY_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class SummaryPromptBuilder:

    def build_chat_summary(
            self,
            previous_summary: str,
            recent_messages: str
        ) -> list[dict]:
        """
        Builds a prompt for generating a chat summary.
        """
        try:
            logger.info("Building chat summary prompt for LLM.")

            messages = [
                {
                    "role": "system",
                    "content": self._build_system_prompt(),
                },
                {
                    "role": "user",
                    "content": self._build_user_prompt(
                        previous_summary=previous_summary,
                        recent_messages=recent_messages,
                    ),
                },
            ]

            logger.info("Chat summary prompt built successfully.")

            return messages
        except Exception as e:
            logger.exception(f"Error building chat summary prompt for LLM: {e}")
            raise RuntimeError(f"Error building chat summary prompt for LLM: {e}")


    def _build_system_prompt(self) -> str:
        """
        Build the system prompt for chat summary.
        """
        return CHAT_SUMMARY_SYSTEM_PROMPT

    def _build_user_prompt(
        self,
        previous_summary: str,
        recent_messages: str
    ) -> str:
        """
        Build the user prompt for chat summary.

        Existing Conversation Summary
        -----------------------------

        <summary>

        -----------------------------

        New Conversation Messages
        -----------------------------

        User:
        ...

        Assistant:
        ...

        User:
        ...

        Assistant:
        ...

        -----------------------------

        Update the conversation summary.
        """
        return (
            "Existing Conversation Summary\n"
            "-----------------------------\n"
            f"{previous_summary}\n\n"
            "-----------------------------\n\n"
            "New Conversation Messages\n"
            "-----------------------------\n"
            f"{recent_messages}\n\n"
            "-----------------------------\n\n"
            "Update the conversation summary."
        )