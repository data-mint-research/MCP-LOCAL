# 📄 Script: graph_executor.py
# 🔧 Zweck: Ausführung des LangGraph für das MCP-System
# 🗂 Pfad: mcp_units/mcp_agent_interaction_engine/graph_executor.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: langgraph
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Dienst führt den LangGraph für das MCP-System aus.
# HINWEIS (MCP): Er stellt eine einfache Schnittstelle zur Verfügung, um
# HINWEIS (MCP): Benutzeranfragen durch den Graph zu verarbeiten.

from typing import Dict
# Change from absolute imports to relative imports
from .graph import build_graph
from .logger import log_event

def invoke_graph(user_input: str, policy: dict = {}) -> dict:
    """
    Invoke the LangGraph with the given user input and policy.
    
    Args:
        user_input: The user's input text
        policy: Optional policy dictionary to control graph behavior
        
    Returns:
        The final state after graph execution
    """
    # Log the graph invocation
    log_event(
        unit="graph_executor",
        level="INFO",
        event="graph_invocation_started",
        message="Starting graph execution",
        input_length=len(user_input),
        has_policy=bool(policy)
    )
    
    try:
        # Prepare the initial state
        state = {"input": user_input, "policy": policy}
        
        # Invoke the graph
        result = build_graph().invoke(state)
        
        # Log successful execution
        log_event(
            unit="graph_executor",
            level="INFO",
            event="graph_invocation_completed",
            message="Graph execution completed successfully",
            output_length=len(result.get("output", "")),
            nodes_visited=len(result.get("nodes_visited", []))
        )
        
        return result
        
    except Exception as e:
        # Log error
        log_event(
            unit="graph_executor",
            level="ERROR",
            event="graph_invocation_failed",
            message=f"Error during graph execution: {str(e)}",
            error=str(e)
        )
        
        # Re-raise the exception
        raise