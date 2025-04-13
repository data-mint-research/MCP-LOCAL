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
from .graph import build_graph

def invoke_graph(user_input: str, policy: dict = {}) -> dict:
    """
    Invoke the LangGraph with the given user input and policy.
    
    Args:
        user_input: The user's input text
        policy: Optional policy dictionary to control graph behavior
        
    Returns:
        The final state after graph execution
    """
    state = {"input": user_input, "policy": policy}
    return build_graph().invoke(state)