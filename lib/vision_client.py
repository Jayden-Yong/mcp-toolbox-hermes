import base64

import httpx

from config import VISION_MODEL_API_KEY, VISION_MODEL_BASE_URL, VISION_MODEL_NAME


def describe_image(image_path: str, prompt: str) -> str:
    """Send an image to the configured vision model and return its text response."""
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    response = httpx.post(
        f"{VISION_MODEL_BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {VISION_MODEL_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": VISION_MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img_b64}"},
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
    return result["choices"][0]["message"]["content"]
