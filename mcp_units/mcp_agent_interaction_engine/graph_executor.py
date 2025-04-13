# 📄 Script: graph_executor.py
# 🔧 Zweck: Ausführungsschnittstelle für den LangGraph
# 🗂 Pfad: mcp_units/mcp_agent_interaction_engine/graph_executor.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: time
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Dienst implementiert die Ausführungsschnittstelle für den LangGraph.
# HINWEIS (MCP): Er stellt eine einfache Funktion bereit, um den Graphen mit Benutzereingaben
# HINWEIS (MCP): und optionalen Richtlinien aufzurufen und die Ergebnisse zurückzugeben.

import time
import logging
import sys
from typing import Dict, Any

# Direct imports since all files are in the same directory
from graph import build_graph
from logger import log_event

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('graph_executor')

def invoke_graph(user_input: str, policy: Dict[str, Any] = {}) -> Dict[str, Any]:
    """
    Invoke the LangGraph with the given user input and policy.
    
    Args:
        user_input: The user's input text
        policy: Optional policy dictionary to control graph behavior
        
    Returns:
        A dictionary containing the graph execution results
    """
    # Log the invocation
    log_event(
        unit="mcp_agent_interaction_engine",
        level="INFO",
        event="GRAPH_INVOKE",
        message=f"Invoking graph with input: {user_input[:50]}...",
        input_length=len(user_input),
        has_policy=bool(policy)
    )
    
    # Record start time
    start_time = time.time()
    
    try:
        # Initialize state
        state = {
            "input": user_input,
            "policy": policy,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        
        # Build and invoke the graph
        graph = build_graph()
        result = graph.invoke(state)
        
        # Calculate duration
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Add execution metadata to result
        result["duration_ms"] = duration_ms
        result["timestamp"] = state["timestamp"]
        result["error"] = None
        
        # Log successful execution
        log_event(
            unit="mcp_agent_interaction_engine",
            level="INFO",
            event="GRAPH_COMPLETE",
            message="Graph execution completed successfully",
            duration_ms=duration_ms,
            nodes_visited=result.get("nodes_visited", [])
        )
        
        return result
        
    except Exception as e:
        # Calculate duration even for failed executions
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Log the error
        error_message = str(e)
        log_event(
            unit="mcp_agent_interaction_engine",
            level="ERROR",
            event="GRAPH_ERROR",
            message=f"Error executing graph: {error_message}",
            duration_ms=duration_ms,
            error=error_message
        )
        
        # Return error information
        return {
            "output": f"Error: {error_message}",
            "nodes_visited": state.get("nodes_visited", []),
            "timestamp": state.get("timestamp", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())),
            "duration_ms": duration_ms,
            "error": error_message
        }