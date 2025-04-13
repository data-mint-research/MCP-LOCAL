# 📄 Script: graph.py
# 🔧 Zweck: LangGraph-Implementierung für das MCP-System
# 🗂 Pfad: mcp_units/mcp_agent_interaction_engine/graph.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: langgraph
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Dienst implementiert den LangGraph für das MCP-System.
# HINWEIS (MCP): Er definiert den Ablauf der Verarbeitung von Benutzeranfragen
# HINWEIS (MCP): durch verschiedene Knoten: MEMORY_LOOKUP → TOOL_DECIDER → 
# HINWEIS (MCP): TOOL_EXECUTE (optional) → LLM_INFER → RESPONSE_FORMATTER

from typing import Dict, Any, Optional
import sys
import os
import logging

# Mock implementations for Docker container networking
import requests
import json
import logging

# Define service URLs based on Docker Compose service names
LLM_SERVICE_URL = "http://llm_infer:5000"
MEMORY_SERVICE_URL = "http://memory_store:5000"
TOOL_SERVICE_URL = "http://executor:5000"

def generate_text(prompt):
    """Mock implementation of generate_text that calls the LLM service via HTTP."""
    try:
        response = requests.post(f"{LLM_SERVICE_URL}/generate", json={"prompt": prompt})
        if response.status_code == 200:
            return response.json().get("text", "")
        else:
            logging.error(f"Failed to generate text: {response.status_code}")
            return f"Error generating text: {response.status_code}"
    except Exception as e:
        logging.error(f"Error calling LLM service: {e}")
        return f"Error: {str(e)}"

def read_memory(key):
    """Mock implementation of read_memory that calls the Memory service via HTTP."""
    try:
        response = requests.get(f"{MEMORY_SERVICE_URL}/memory/{key}")
        if response.status_code == 200:
            return response.json().get("data")
        else:
            logging.error(f"Failed to read memory: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error calling Memory service: {e}")
        return None

def write_memory(key, data):
    """Mock implementation of write_memory that calls the Memory service via HTTP."""
    try:
        response = requests.post(f"{MEMORY_SERVICE_URL}/memory/{key}", json={"data": data})
        if response.status_code == 200:
            return True
        else:
            logging.error(f"Failed to write memory: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"Error calling Memory service: {e}")
        return False

def run_shell_command(command):
    """Mock implementation of run_shell_command that calls the Tool service via HTTP."""
    try:
        response = requests.post(f"{TOOL_SERVICE_URL}/execute", json={"command": command})
        if response.status_code == 200:
            return response.json().get("result", "")
        else:
            logging.error(f"Failed to run command: {response.status_code}")
            return f"Error running command: {response.status_code}"
    except Exception as e:
        logging.error(f"Error calling Tool service: {e}")
        return f"Error: {str(e)}"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('graph')

# Define the graph nodes
def memory_lookup(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Look up relevant information from memory based on the user input.
    
    Args:
        state: The current state dictionary containing at least 'input' key
        
    Returns:
        Updated state with memory information
    """
    user_input = state.get("input", "")
    logger.info(f"Memory lookup for input: {user_input[:50]}...")
    
    # Retrieve context from memory if available
    context = read_memory("context") or {}
    history = read_memory("conversation_history") or []
    
    # Update state with memory information
    state["context"] = context
    state["history"] = history
    state["nodes_visited"] = ["MEMORY_LOOKUP"]
    
    return state

def tool_decider(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decide whether to use a tool based on the policy and user input.
    
    Args:
        state: The current state dictionary
        
    Returns:
        Updated state with tool decision
    """
    policy = state.get("policy", {})
    use_tool = policy.get("use_tool", False)
    
    logger.info(f"Tool decision: {use_tool}")
    
    # Update state with tool decision
    state["use_tool"] = use_tool
    state["nodes_visited"].append("TOOL_DECIDER")
    
    return state

def tool_execute(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the appropriate tool based on the user input and policy.
    
    Args:
        state: The current state dictionary
        
    Returns:
        Updated state with tool execution results
    """
    if not state.get("use_tool", False):
        return state
    
    user_input = state.get("input", "")
    policy = state.get("policy", {})
    tool_command = policy.get("tool_command", "")
    
    logger.info(f"Executing tool: {tool_command}")
    
    # Execute the tool command
    try:
        tool_result = run_shell_command(tool_command)
        state["tool_result"] = tool_result
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        state["tool_result"] = f"Error executing tool: {str(e)}"
    
    state["nodes_visited"].append("TOOL_EXECUTE")
    
    return state

def llm_infer(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a response using the LLM based on the user input and context.
    
    Args:
        state: The current state dictionary
        
    Returns:
        Updated state with LLM response
    """
    user_input = state.get("input", "")
    context = state.get("context", {})
    history = state.get("history", [])
    tool_result = state.get("tool_result", "")
    
    # Construct prompt with context, history, and tool result if available
    prompt = f"User input: {user_input}\n"
    
    if context:
        prompt += f"Context: {context}\n"
    
    if history:
        prompt += "Conversation history:\n"
        for entry in history[-3:]:  # Include last 3 entries
            prompt += f"- {entry}\n"
    
    if tool_result:
        prompt += f"Tool result: {tool_result}\n"
    
    logger.info(f"Generating LLM response for prompt: {prompt[:50]}...")
    
    # Generate response using LLM
    llm_response = generate_text(prompt)
    state["llm_response"] = llm_response
    state["nodes_visited"].append("LLM_INFER")
    
    # Update conversation history in memory
    history.append({"user": user_input, "system": llm_response})
    write_memory("conversation_history", history)
    
    return state

def response_formatter(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format the final response to be returned to the user.
    
    Args:
        state: The current state dictionary
        
    Returns:
        Updated state with formatted response
    """
    llm_response = state.get("llm_response", "")
    tool_result = state.get("tool_result", "")
    
    # Format the response
    if tool_result:
        formatted_response = f"Tool output: {tool_result}\n\nResponse: {llm_response}"
    else:
        formatted_response = llm_response
    
    state["output"] = formatted_response
    state["nodes_visited"].append("RESPONSE_FORMATTER")
    
    return state

def should_use_tool(state: Dict[str, Any]) -> bool:
    """
    Determine whether to use a tool based on the state.
    
    Args:
        state: The current state dictionary
        
    Returns:
        Boolean indicating whether to use a tool
    """
    return state.get("use_tool", False)

def build_graph():
    """
    Build and return the LangGraph for the MCP system.
    
    Returns:
        A LangGraph instance with the defined nodes and edges
    """
    from langgraph.graph import StateGraph
    
    # Create a new graph
    graph = StateGraph(Dict[str, Any])
    
    # Add nodes to the graph
    graph.add_node("memory_lookup", memory_lookup)
    graph.add_node("tool_decider", tool_decider)
    graph.add_node("tool_execute", tool_execute)
    graph.add_node("llm_infer", llm_infer)
    graph.add_node("response_formatter", response_formatter)
    
    # Define the edges between nodes
    graph.add_edge("memory_lookup", "tool_decider")
    graph.add_conditional_edges(
        "tool_decider",
        should_use_tool,
        {
            True: "tool_execute",
            False: "llm_infer"
        }
    )
    graph.add_edge("tool_execute", "llm_infer")
    graph.add_edge("llm_infer", "response_formatter")
    
    # Set the entry point
    graph.set_entry_point("memory_lookup")
    
    # Compile the graph
    return graph.compile()