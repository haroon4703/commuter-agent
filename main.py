from fastapi import FastAPI
from models import AgentRequest, AgentResponse, Status
from agent_graph import app_graph
from registry import register_agent
from config import Config
import uvicorn
from contextlib import asynccontextmanager
import asyncio
from utils import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    register_agent()
    yield
    # Shutdown

app = FastAPI(title=Config.AGENT_NAME, lifespan=lifespan)

@app.get("/")
def root():
    """
    Root endpoint providing API information.
    """
    return {
        "agent_name": "commuter-agent",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "agent": "/commuter-agent"
        },
        "description": "AI Commuter Assistance Agent - Provides route planning, traffic updates, and travel mode suggestions"
    }

@app.post("/commuter-agent", response_model=AgentResponse)
async def agent_endpoint(request: AgentRequest):
    """
    Main endpoint for commuter agent. Accepts messages and returns structured response.
    Always returns JSON, never crashes.
    """
    try:
        # Validate input
        if not request.messages:
            return AgentResponse(
                agent_name="commuter-agent",
                status=Status.ERROR,
                data=None,
                error_message="No messages provided"
            )
        
        # Convert messages to dict format
        try:
            inputs = {"messages": [m.dict() for m in request.messages]}
        except Exception as e:
            logger.error(f"Error converting messages: {e}")
            return AgentResponse(
                agent_name="commuter-agent",
                status=Status.ERROR,
                data=None,
                error_message=f"Invalid message format: {str(e)}"
            )
        
        # Process with timeout (5 seconds)
        try:
            result = await asyncio.wait_for(
                asyncio.to_thread(app_graph.invoke, inputs),
                timeout=5.0
            )
            
            # Extract response from result
            if "response" not in result:
                return AgentResponse(
                    agent_name="commuter-agent",
                    status=Status.ERROR,
                    data=None,
                    error_message="Invalid response format from agent graph"
                )
            
            response_data = result["response"]
            
            # Ensure response is properly formatted
            if isinstance(response_data, dict):
                # If it's already an AgentResponse dict, return it
                if "agent_name" in response_data and "status" in response_data:
                    return AgentResponse(**response_data)
                # Otherwise wrap it in message
                return AgentResponse(
                    agent_name="commuter-agent",
                    status=Status.SUCCESS,
                    data={"message": response_data},
                    error_message=None
                )
            else:
                return AgentResponse(
                    agent_name="commuter-agent",
                    status=Status.SUCCESS,
                    data={"message": str(response_data)},
                    error_message=None
                )
                
        except asyncio.TimeoutError:
            logger.error("Agent processing timed out")
            return AgentResponse(
                agent_name="commuter-agent",
                status=Status.ERROR,
                data=None,
                error_message="Request processing timed out"
            )
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return AgentResponse(
                agent_name="commuter-agent",
                status=Status.ERROR,
                data=None,
                error_message=str(e)
            )
            
    except Exception as e:
        # Catch-all for any unexpected errors
        logger.error(f"Unexpected error in agent endpoint: {e}")
        return AgentResponse(
            agent_name="commuter-agent",
            status=Status.ERROR,
            data=None,
            error_message=f"Internal error: {str(e)}"
        )

@app.get("/health")
def health_check():
    """
    Health check endpoint. Returns agent status.
    """
    return {
        "status": "ok",
        "agent_name": "commuter-agent",
        "ready": True
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host=Config.API_HOST, port=Config.API_PORT, reload=True)
