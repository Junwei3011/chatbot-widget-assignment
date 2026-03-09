from __future__ import annotations

from typing import List

from google import genai
from google.genai import types

from config import get_settings
from models import ChatMessage


PROMPT_TEMPLATE = """You are a helpful website chatbot.

Rules:
- Answer clearly and concisely.
- If the user's question is about OWASP, API security, web security, or application security, prioritize the retrieved OWASP context when it is relevant.
- Do not invent OWASP facts that are not supported by the retrieved context.
- If the retrieved context is not relevant, answer the user normally.
- Keep answers practical and easy to understand.

Conversation history:
{history}

Retrieved OWASP context:
{context}

Current user message:
{message}
"""


def _format_history(history: List[ChatMessage]) -> str:
    if not history:
        return "No previous messages."
    return "\n".join(f"{item.role.title()}: {item.text}" for item in history)


class GeminiService:
    def __init__(self):
        settings = get_settings()
        self.model_name = settings.gemini_model
        self.enabled = bool(settings.gemini_api_key)
        self.client = genai.Client(api_key=settings.gemini_api_key) if self.enabled else None

    def generate_reply(self, message: str, history: List[ChatMessage], rag_context: str) -> str:
        prompt = PROMPT_TEMPLATE.format(
            history=_format_history(history),
            context=rag_context,
            message=message,
        )

        if not self.enabled:
            return (
                "Gemini is not configured yet. Add GEMINI_API_KEY to backend/.env. "
                f"Here is the retrieved OWASP context I found:\n\n{rag_context}"
            )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=500),
        )
        return (response.text or "I could not generate a response right now.").strip()
