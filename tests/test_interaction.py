# 📄 Script: test_interaction.py
# 🔧 Zweck: Testfälle für die Anwendung
# 🗂 Pfad: tests/test_interaction.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: mcp_units.mcp_agent_interaction_engine.dialog_flow
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Test überprüft die Funktionalität der handle_input-Funktion
# HINWEIS (MCP): der Agent-Interaktions-Engine. Er stellt sicher, dass die Engine
# HINWEIS (MCP): korrekt auf Benutzereingaben reagiert und die erwarteten Antworten
# HINWEIS (MCP): zurückgibt. Dies ist ein grundlegender Test für die Dialogverarbeitung.

from mcp_units.mcp_agent_interaction_engine.dialog_flow import handle_input
import pytest

def test_handle_input():
    assert "Echo" in handle_input("Hallo")

# HINWEIS (MCP): Hinzugefügt für direkte Ausführbarkeit des Tests
# HINWEIS (MCP): Verwendet absolute Pfade, um von jedem Verzeichnis aus ausführbar zu sein
if __name__ == "__main__":
    pytest.main(["-v", __file__])