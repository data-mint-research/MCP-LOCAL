# 📄 Script: test_memory.py
# 🔧 Zweck: Testfälle für die Anwendung
# 🗂 Pfad: tests/test_memory.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: mcp_units.mcp_host_memory_store.memory_handler
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Test überprüft die Funktionalität des Memory-Store-Dienstes.
# HINWEIS (MCP): Er testet den vollständigen Zyklus von Laden, Schreiben und Lesen
# HINWEIS (MCP): von Daten im Speicher und stellt sicher, dass die Persistenzfunktionen
# HINWEIS (MCP): korrekt arbeiten. Dies ist ein kritischer Test für die Datenspeicherung
# HINWEIS (MCP): und -verwaltung im MCP-System.

from mcp_units.mcp_host_memory_store.memory_handler import write_memory, read_memory, load_memory
import pytest

def test_memory_cycle():
    load_memory()
    write_memory("foo", "bar")
    assert read_memory("foo") == "bar"

# HINWEIS (MCP): Hinzugefügt für direkte Ausführbarkeit des Tests
# HINWEIS (MCP): Verwendet absolute Pfade, um von jedem Verzeichnis aus ausführbar zu sein
if __name__ == "__main__":
    pytest.main(["-v", __file__])