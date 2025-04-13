# 📄 Script: test_registry.py
# 🔧 Zweck: Testfälle für die Anwendung
# 🗂 Pfad: tests/test_registry.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: yaml
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Test überprüft, ob die MCP-Registrierungsdatei korrekt
# HINWEIS (MCP): geladen werden kann und die erwartete Struktur aufweist.
# HINWEIS (MCP): Er stellt sicher, dass die Registrierung der MCP-Einheiten
# HINWEIS (MCP): ordnungsgemäß erfolgt ist und die Datei gültig ist.
# HINWEIS (MCP): Dies ist ein grundlegender Test für die MCP-Konfiguration.

import yaml
import pytest
import os

def test_registry_loads():
    # Get the directory of this file
    test_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root
    project_root = os.path.dirname(test_dir)
    # Construct the path to the registry file
    registry_path = os.path.join(project_root, "config", "mcp_register.yaml")
    
    with open(registry_path) as f:
        data = yaml.safe_load(f)
        assert "units" in data

# HINWEIS (MCP): Hinzugefügt für direkte Ausführbarkeit des Tests
# HINWEIS (MCP): Verwendet absolute Pfade, um von jedem Verzeichnis aus ausführbar zu sein
if __name__ == "__main__":
    pytest.main(["-v", __file__])