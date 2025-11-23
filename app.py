"""
Hugging Face Spaces entry point for Commuter Agent.
This file is used by Hugging Face Spaces to deploy the FastAPI application.
For Docker deployments, the Dockerfile handles the server startup.
"""
from main import app

# Export the FastAPI app for Hugging Face Spaces
# Hugging Face will automatically detect and serve the FastAPI app

