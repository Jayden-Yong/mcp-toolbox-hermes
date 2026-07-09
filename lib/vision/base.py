from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class TokenUsage:
    """Standardized representation of API token usage."""
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

@dataclass
class VisionResponse:
    """Model-agnostic and provider-agnostic response container."""
    text: str
    model: str
    provider: str
    usage: TokenUsage = field(default_factory=TokenUsage)
    raw_response: Dict[str, any] = field(default_factory=dict)

@dataclass
class VisionProvider(ABC):
    """Abstract Base Class for Vision API providers."""

    @abstractmethod
    def describe_image(self, image_path: str, prompt: str) -> VisionResponse:
        """Sends an image to the model and returns a standardized VisionResponse."""
        pass