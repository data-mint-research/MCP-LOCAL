# 📄 Script: test_status_ping.py
# 🔧 Zweck: Testfälle für die Anwendung
# 🗂 Pfad: tests/test_status_ping.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: json
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Test überprüft die Struktur der Status-Datei des MCP-Systems.
# HINWEIS (MCP): Er stellt sicher, dass die Datei korrekt formatiert ist und die
# HINWEIS (MCP): erforderlichen Informationen über die MCP-Einheiten enthält.
# HINWEIS (MCP): Dies ist ein wichtiger Test für die Überwachung und Diagnose
# HINWEIS (MCP): des Systemzustands im MCP-Framework.

import json
import pytest
import os

def test_status_structure():
    # Get the directory of this file
    test_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root
    project_root = os.path.dirname(test_dir)
    # Construct the path to the status file
    status_path = os.path.join(project_root, "runtime_state", "state_status.json")
    
    with open(status_path) as f:
        status = json.load(f)
        assert "units" in status
        assert isinstance(status["units"], dict)

# HINWEIS (MCP): Hinzugefügt für direkte Ausführbarkeit des Tests
# HINWEIS (MCP): Verwendet absolute Pfade, um von jedem Verzeichnis aus ausführbar zu sein
if __name__ == "__main__":
    pytest.main(["-v", __file__])