# 📄 Script: test_registry.py
# 🔧 Zweck: Testfälle für die Anwendung
# 🗂 Pfad: tests/test_registry.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: yaml
# 🧪 Testbar: ❌

import yaml

def test_registry_loads():
    with open("MCP-LOCAL/config/mcp_register.yaml") as f:
        data = yaml.safe_load(f)
        assert "units" in data