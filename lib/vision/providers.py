import base64

import httpx

from lib.vision.base import TokenUsage, VisionProvider, VisionResponse


class OpenAICompatibleProvider(VisionProvider):
    """Provider for OpenAI-compatible Chat Completions Vision endpoints (e.g. OpenCode Zen, OpenRouter)."""

    def __init__(self, base_url: str, api_key: str, model_name: str):
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name

    def describe_image(self, image_path: str, prompt: str) -> VisionResponse:
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()

        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_b64}"
                                },
                            },
                        ],
                    }
                ],
                "max_tokens": 4096,
            },
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()
        usage_data = result.get("usage", {})
        usage = TokenUsage(
            prompt_tokens=usage_data.get("prompt_tokens"),
            completion_tokens=usage_data.get("completion_tokens"),
            total_tokens=usage_data.get("total_tokens"),
        )

        return VisionResponse(
            text=result["choices"][0]["message"]["content"],
            model=self.model_name,
            provider="openai-compatible",
            usage=usage,
            raw_response=result,
        )
