import os

from dotenv import load_dotenv

load_dotenv()

# Vison model settings
VISION_MODEL_API_KEY = os.getenv("OPENCODE_ZEN_API_KEY", "")
VISION_MODEL_NAME = os.getenv("VISION_MODEL_NAME", "mimo-v2.5-free")
VISION_MODEL_BASE_URL = os.getenv("VISION_MODEL_BASE_URL", "https://opencode.ai/zen/v1")

# MCP server transport settings
_port_raw = os.getenv("MCP_PORT")
MCP_PORT = int(_port_raw) if _port_raw else 8931
