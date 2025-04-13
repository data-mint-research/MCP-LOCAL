# 📄 Script: test_status_ping.py
# 🔧 Zweck: Testfälle für die Anwendung
# 🗂 Pfad: tests/test_status_ping.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: json
# 🧪 Testbar: ❌

import json

def test_status_structure():
    with open("MCP-LOCAL/runtime_state/state_status.json") as f:
        status = json.load(f)
        assert "units" in status
        assert isinstance(status["units"], dict)