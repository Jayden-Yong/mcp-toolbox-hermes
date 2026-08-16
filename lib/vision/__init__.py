from lib.vision.base import TokenUsage, VisionProvider, VisionResponse
from lib.vision.client import VisionClient

__all__ = [
    "TokenUsage",
    "VisionClient",
    "VisionProvider",
    "VisionResponse",
    "describe_image",
]


def describe_image(image_path: str, prompt: str) -> str:
    """
    Backward-compatible helper function that returns the text description directly as a string.
    """
    client = VisionClient.from_env()
    response = client.describe_image(image_path, prompt)
    return response.text
