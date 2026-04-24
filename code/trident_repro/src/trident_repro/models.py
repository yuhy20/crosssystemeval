"""Chat-client adapters for Anthropic, OpenAI, and Groq-hosted open-weight.

All clients implement the minimal `ChatClient` Protocol so the rest of the
package is provider-agnostic and trivially mockable in tests.

Retries: tenacity with exponential backoff on transient API errors
(`RateLimitError`, `APIConnectionError`, and generic timeouts).
"""

from __future__ import annotations

import logging
from typing import Any, Protocol, runtime_checkable

import anthropic
import openai

from trident_repro.config import GROQ_BASE_URL
from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Retry policy
# ---------------------------------------------------------------------------

# Transient errors worth retrying.
_RETRYABLE: tuple[type[BaseException], ...] = (
    anthropic.RateLimitError,
    anthropic.APIConnectionError,
    anthropic.APITimeoutError,
    openai.RateLimitError,
    openai.APIConnectionError,
    openai.APITimeoutError,
)


def _log_retry(state: RetryCallState) -> None:
    """tenacity before_sleep hook: log the reason + attempt number."""
    exc = state.outcome.exception() if state.outcome else None
    logger.warning(
        "retrying %s (attempt %d) after %s",
        state.fn.__name__ if state.fn else "<unknown>",
        state.attempt_number,
        type(exc).__name__ if exc else "unknown error",
    )


_retry_decorator = retry(
    reraise=True,
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=30),
    retry=retry_if_exception_type(_RETRYABLE),
    before_sleep=_log_retry,
)


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class ChatClient(Protocol):
    """Minimal chat completion interface used throughout the package."""

    model: str

    def complete(
        self,
        *,
        system: str,
        user: str,
        max_tokens: int = 1024,
        temperature: float = 0.0,
    ) -> str:
        """Return the assistant text for the given system+user messages."""
        ...


# ---------------------------------------------------------------------------
# Anthropic
# ---------------------------------------------------------------------------


class AnthropicChatClient:
    """Thin wrapper around the Anthropic Messages API."""

    def __init__(self, api_key: str, model: str) -> None:
        if not api_key:
            raise ValueError("AnthropicChatClient requires a non-empty api_key")
        self.model: str = model
        self._client: anthropic.Anthropic = anthropic.Anthropic(api_key=api_key)

    @_retry_decorator
    def complete(
        self,
        *,
        system: str,
        user: str,
        max_tokens: int = 1024,
        temperature: float = 0.0,
    ) -> str:
        logger.debug(
            "anthropic.messages.create model=%s max_tokens=%d temp=%.2f",
            self.model,
            max_tokens,
            temperature,
        )
        response = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        text = _extract_anthropic_text(response)
        usage = getattr(response, "usage", None)
        if usage is not None:
            logger.info(
                "anthropic.ok model=%s input_tokens=%s output_tokens=%s",
                self.model,
                getattr(usage, "input_tokens", "?"),
                getattr(usage, "output_tokens", "?"),
            )
        return text


def _extract_anthropic_text(response: Any) -> str:
    """Pull the concatenated text from an Anthropic Messages response."""
    parts: list[str] = []
    for block in getattr(response, "content", []) or []:
        text = getattr(block, "text", None)
        if text is not None:
            parts.append(text)
    return "".join(parts).strip()


# ---------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------


class OpenAIChatClient:
    """Thin wrapper around OpenAI Chat Completions.

    Also usable against any OpenAI-compatible endpoint via `base_url`
    (Groq, Together, Fireworks, etc.).
    """

    def __init__(
        self,
        api_key: str,
        model: str,
        *,
        base_url: str | None = None,
    ) -> None:
        if not api_key:
            raise ValueError("OpenAIChatClient requires a non-empty api_key")
        self.model: str = model
        self._client: openai.OpenAI = openai.OpenAI(api_key=api_key, base_url=base_url)

    @_retry_decorator
    def complete(
        self,
        *,
        system: str,
        user: str,
        max_tokens: int = 1024,
        temperature: float = 0.0,
    ) -> str:
        logger.debug(
            "openai.chat.completions.create model=%s max_tokens=%d temp=%.2f",
            self.model,
            max_tokens,
            temperature,
        )
        response = self._client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        choice = response.choices[0]
        text = (choice.message.content or "").strip()
        usage = getattr(response, "usage", None)
        if usage is not None:
            logger.info(
                "openai.ok model=%s prompt_tokens=%s completion_tokens=%s",
                self.model,
                getattr(usage, "prompt_tokens", "?"),
                getattr(usage, "completion_tokens", "?"),
            )
        return text


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def build_client(
    model: str,
    *,
    anthropic_key: str | None,
    openai_key: str | None,
    groq_key: str | None = None,
) -> ChatClient:
    """Return the correct `ChatClient` for a given model id.

    Routing (first match wins):
      - ``claude*`` → Anthropic
      - ``gemma*``, ``llama*`` → Groq (OpenAI-compatible API)
      - everything else → OpenAI
    """
    lower = model.lower()
    if lower.startswith("claude"):
        if not anthropic_key:
            raise RuntimeError(f"ANTHROPIC_API_KEY required to use model {model!r}")
        return AnthropicChatClient(api_key=anthropic_key, model=model)
    if lower.startswith(("gemma", "llama")):
        if not groq_key:
            raise RuntimeError(
                f"GROQ_API_KEY required to use model {model!r}. "
                "Sign up at https://console.groq.com and add GROQ_API_KEY to .env."
            )
        return OpenAIChatClient(api_key=groq_key, model=model, base_url=GROQ_BASE_URL)
    if not openai_key:
        raise RuntimeError(f"OPENAI_API_KEY required to use model {model!r}")
    return OpenAIChatClient(api_key=openai_key, model=model)
