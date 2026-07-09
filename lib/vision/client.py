from lib.vision.base import VisionProvider, VisionResponse
from lib.vision.providers import OpenAICompatibleProvider

class VisionClient:
    """Orchestrates API requests by routing them to concrete VisionProviders."""
    def __init__(self, provider: VisionProvider):
        self.provider = provider

    def describe_image(self, image_path: str, prompt: str) -> VisionResponse:
        return self.provider.describe_image(image_path, prompt)

    @classmethod
    def from_env(cls) -> "VisionClient":
        """Factory method to build a VisionClient from system config/env variables."""
        from config import VISION_MODEL_API_KEY, VISION_MODEL_NAME, VISION_MODEL_BASE_URL

        base_url_lower = VISION_MODEL_BASE_URL.lower()
        model_name_lower = VISION_MODEL_NAME.lower()

        """
        if "anthropic" in base_url_lower or "claude" in model_name_lower:
            provider = AnthropicProvider(
                api_key=VISION_MODEL_API_KEY,
                model_name=VISION_MODEL_NAME
            )
        else:
            provider = OpenAICompatibleProvider(
                base_url=VISION_MODEL_BASE_URL,
                api_key=VISION_MODEL_API_KEY,
                model_name=VISION_MODEL_NAME
            )
        """

        provider = OpenAICompatibleProvider(
            base_url=VISION_MODEL_BASE_URL,
            api_key=VISION_MODEL_API_KEY,
            model_name=VISION_MODEL_NAME
        )

        return cls(provider)