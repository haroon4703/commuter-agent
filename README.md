---
title: Commuter Agent
emoji: 🚗
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: apache-2.0
short_description: An AI agent that provides intelligent commuter assistance including route planning, traffic updates, and travel mode suggestions.
---

# Commuter Assistance Agent

## Overview

This agent provides route recommendations, traffic updates, and travel mode suggestions. It is built with FastAPI and LangGraph.

## Setup

### Local

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   python main.py
   ```

### Docker

1. Build the image:
   ```bash
   docker build -t commuter-agent .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 commuter-agent
   ```

## API

- `POST /commuter-agent`: Main endpoint for agent interaction. Accepts messages and returns structured JSON response.
- `GET /health`: Health check endpoint. Returns agent status.

## Configuration

Set environment variables in `.env` or Docker environment.

- `API_HOST`: Host to bind (default 0.0.0.0)
- `API_PORT`: Port to bind (default 8000)
- `SUPERVISOR_URL`: URL of the supervisor agent
- `GOOGLE_MAPS_API_KEY`: Google Maps API key for real-time route and traffic data (optional - falls back to mock data if not provided)

### Google Maps API Setup

1. Get a Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the following APIs:
   - Directions API
   - Distance Matrix API
   - Maps JavaScript API (optional)
3. Add the key to your `.env` file:
   ```
   GOOGLE_MAPS_API_KEY=your_api_key_here
   ```

**Note:** If no API key is provided, the agent will use mock data for demonstrations.
