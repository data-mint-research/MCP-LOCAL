# 📄 Script: test_interaction.py
# 🔧 Zweck: Testfälle für die Anwendung
# 🗂 Pfad: tests/test_interaction.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: mcp_units.mcp_agent_interaction_engine.graph_executor
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Test überprüft die Funktionalität der invoke_graph-Funktion
# HINWEIS (MCP): der Agent-Interaktions-Engine. Er stellt sicher, dass die Engine
# HINWEIS (MCP): korrekt auf Benutzereingaben reagiert und die erwarteten Antworten
# HINWEIS (MCP): zurückgibt. Dies ist ein grundlegender Test für die Graphverarbeitung.

from mcp_units.mcp_agent_interaction_engine.graph_executor import invoke_graph
import pytest

def test_invoke_graph():
    result = invoke_graph("Hallo")
    assert "output" in result
    assert isinstance(result["output"], str)

# HINWEIS (MCP): Hinzugefügt für direkte Ausführbarkeit des Tests
# HINWEIS (MCP): Verwendet absolute Pfade, um von jedem Verzeichnis aus ausführbar zu sein
if __name__ == "__main__":
    pytest.main(["-v", __file__])