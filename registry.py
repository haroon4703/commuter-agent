import requests
from config import Config
from utils import logger

def register_agent():
    """
    Registers the agent with the Supervisor.
    """
    payload = {
        "agent_id": Config.AGENT_ID,
        "agent_name": Config.AGENT_NAME,
        "api_url": f"http://{Config.API_HOST}:{Config.API_PORT}/commuter-agent",
        "capabilities": ["route_planning", "traffic_updates", "travel_mode_suggestion", "commute_optimization", "navigation_assistance"],
        "status": "active"
    }
    try:
        logger.info(f"Attempting to register agent at {Config.SUPERVISOR_URL}")
        # In a real scenario, we would uncomment the following lines:
        # response = requests.post(Config.SUPERVISOR_URL, json=payload)
        # response.raise_for_status()
        # logger.info("Agent registered successfully.")
        logger.info("Agent registration simulated (Supervisor URL not reachable in this env).")
    except Exception as e:
        logger.error(f"Failed to register agent: {e}")
