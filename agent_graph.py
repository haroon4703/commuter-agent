from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any
from models import AgentResponse, Status
from commuter_agent import CommuterAgentLogic
from utils import logger

class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    response: Dict[str, Any]

logic = CommuterAgentLogic()

def process_request(state: AgentState):
    """
    Process the request using LangGraph. Returns structured response.
    """
    messages = state.get('messages', [])
    if not messages:
        response = AgentResponse(
            agent_name="commuter-agent",
            status=Status.ERROR,
            data=None,
            error_message="No messages provided"
        )
        return {"response": response.dict()}
        
    # Get the last user message
    last_message = ""
    for msg in reversed(messages):
        if msg.get('role') == 'user':
            last_message = msg.get('content', '')
            break
    
    if not last_message:
        response = AgentResponse(
            agent_name="commuter-agent",
            status=Status.ERROR,
            data=None,
            error_message="No user message found in messages"
        )
        return {"response": response.dict()}
    
    logger.info(f"Processing message: {last_message}")
    
    try:
        result = logic.process_query(last_message)
        # Wrap result in message format as per requirements
        response = AgentResponse(
            agent_name="commuter-agent",
            status=Status.SUCCESS,
            data={"message": result},
            error_message=None
        )
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        response = AgentResponse(
            agent_name="commuter-agent",
            status=Status.ERROR,
            data=None,
            error_message=str(e)
        )
        
    return {"response": response.dict()}

workflow = StateGraph(AgentState)
workflow.add_node("agent", process_request)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

app_graph = workflow.compile()
