import requests
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class OllamaClient:
    """
    Phase 2 - Agentic AI Core Library
    HTTP client wrapper for the Ollama local LLM server.

    Supports:
      - chat()    : single-turn or multi-turn conversation via /api/chat
      - generate(): raw completion via /api/generate
      - list_models(): list available Ollama models

    Default base_url assumes Ollama running locally on port 11434.
    """

    DEFAULT_BASE_URL = "http://localhost:11434"
    DEFAULT_MODEL = "llama3"
    DEFAULT_TIMEOUT = 120  # seconds

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        model: str = DEFAULT_MODEL,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def chat(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """
        Send a chat message to Ollama and return the assistant reply as a string.

        Args:
            prompt: User message content.
            system_prompt: Optional system-level instruction.
            history: Optional prior messages [{"role": ..., "content": ...}].
            model: Override the instance model for this request.
            temperature: Sampling temperature (0.0 = deterministic).

        Returns:
            Assistant reply string, or empty string on error.
        """
        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model or self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }
        try:
            resp = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout,
            )
            resp.raise_for_status()
            data = resp.json()
            reply = data.get("message", {}).get("content", "")
            self.logger.debug("[OllamaClient] chat reply (%d chars)", len(reply))
            return reply
        except requests.exceptions.ConnectionError:
            self.logger.error(
                "[OllamaClient] Cannot connect to Ollama at %s. Is it running?",
                self.base_url,
            )
            return ""
        except requests.exceptions.Timeout:
            self.logger.error("[OllamaClient] Request timed out after %ds", self.timeout)
            return ""
        except Exception as exc:
            self.logger.error("[OllamaClient] chat error: %s", exc)
            return ""

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """
        Raw text completion via /api/generate.
        Returns the generated text, or empty string on error.
        """
        payload: Dict[str, Any] = {
            "model": model or self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if system_prompt:
            payload["system"] = system_prompt
        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )
            resp.raise_for_status()
            return resp.json().get("response", "")
        except Exception as exc:
            self.logger.error("[OllamaClient] generate error: %s", exc)
            return ""

    def list_models(self) -> List[str]:
        """
        Return a list of model names available on the Ollama server.
        Returns empty list on error.
        """
        try:
            resp = requests.get(
                f"{self.base_url}/api/tags", timeout=10
            )
            resp.raise_for_status()
            models = resp.json().get("models", [])
            return [m.get("name", "") for m in models]
        except Exception as exc:
            self.logger.error("[OllamaClient] list_models error: %s", exc)
            return []

    def is_available(self) -> bool:
        """Return True if the Ollama server is reachable."""
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return resp.status_code == 200
        except Exception:
            return False
