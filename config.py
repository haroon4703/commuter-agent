import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AGENT_NAME = "commuter-agent"
    AGENT_ID = "commuter_agent_01"
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    # Hugging Face Spaces uses port 7860, but we'll use environment variable
    API_PORT = int(os.getenv("API_PORT", os.getenv("PORT", 8000)))
    SUPERVISOR_URL = os.getenv("SUPERVISOR_URL", "http://supervisor-agent/register")
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
