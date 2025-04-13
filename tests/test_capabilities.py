# 📄 Script: test_capabilities.py
# 🔧 Zweck: Testfälle für die Anwendung
# 🗂 Pfad: tests/test_capabilities.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: yaml
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Test überprüft, ob die MCP-Agent-Interaktions-Engine
# HINWEIS (MCP): die erforderlichen Fähigkeiten gemäß den Capability-Regeln besitzt.
# HINWEIS (MCP): Er ist Teil der MCP-Compliance-Tests und stellt sicher, dass
# HINWEIS (MCP): die Komponenten die richtigen Fähigkeiten deklarieren.

import yaml
import pytest
import os

def test_agent_has_capabilities():
    # Get the directory of this file
    test_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root
    project_root = os.path.dirname(test_dir)
    # Construct the path to the capabilities file
    capabilities_path = os.path.join(project_root, "config", "rules", "capabilities.rules.yaml")
    
    with open(capabilities_path) as f:
        caps = yaml.safe_load(f)
    assert "mcp_agent_interaction_engine" in caps.get("capabilities", {})

# HINWEIS (MCP): Hinzugefügt für direkte Ausführbarkeit des Tests
# HINWEIS (MCP): Verwendet absolute Pfade, um von jedem Verzeichnis aus ausführbar zu sein
if __name__ == "__main__":
    pytest.main(["-v", __file__])