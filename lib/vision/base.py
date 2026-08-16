from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TokenUsage:
    """Standardized representation of API token usage."""

    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


@dataclass
class VisionResponse:
    """Model-agnostic and provider-agnostic response container."""

    text: str
    model: str
    provider: str
    usage: TokenUsage = field(default_factory=TokenUsage)
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionProvider(ABC):
    """Abstract Base Class for Vision API providers."""

    @abstractmethod
    def describe_image(self, image_path: str, prompt: str) -> VisionResponse:
        """Sends an image to the model and returns a standardized VisionResponse."""
