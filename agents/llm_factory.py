"""
Deterministic mock response provider. External LLM integrations are not implemented.
"""
from typing import Dict, Any, Optional
from .base import PHIGuard


class MockLLM:
    def __init__(self, system_name: str = "Fermentation Gas Mass Spectrometry"):
        self.system_name = system_name

    def invoke(self, prompt: str) -> str:
        PHIGuard.assert_no_phi(prompt)
        return f"[{self.system_name} mock]: No scientific or LLM analysis performed. Query received: {prompt[:60]!r}."


class LLMFactory:
    """Only deterministic mock mode is available; other providers fail explicitly."""

    @staticmethod
    def create(provider: str = "mock", system_name: str = "Fermentation Gas Mass Spectrometry"):
        prov = str(provider).lower()
        if prov in ["mock", "deterministic", "test"]:
            return MockLLM(system_name)
        if prov in ["ollama", "local", "claude", "anthropic", "openai", "gpt4"]:
            raise ValueError(f"Provider {provider!r} is not implemented; use 'mock'.")
        raise ValueError(f"Unknown provider: {provider!r}")
