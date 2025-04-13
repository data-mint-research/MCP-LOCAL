# 📄 Script: test_capabilities.py
# 🔧 Zweck: Testfälle für die Anwendung
# 🗂 Pfad: tests/test_capabilities.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: yaml
# 🧪 Testbar: ❌

import yaml

def test_agent_has_capabilities():
    with open("MCP-LOCAL/config/rules/capabilities.rules.yaml") as f:
        caps = yaml.safe_load(f)
    assert "mcp_agent_interaction_engine" in caps.get("capabilities", {})