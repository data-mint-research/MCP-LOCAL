# 📄 Script: test_memory.py
# 🔧 Zweck: Testfälle für die Anwendung
# 🗂 Pfad: tests/test_memory.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: mcp_units.mcp_host_memory_store.memory_handler
# 🧪 Testbar: ❌

from mcp_units.mcp_host_memory_store.memory_handler import write_memory, read_memory, load_memory

def test_memory_cycle():
    load_memory()
    write_memory("foo", "bar")
    assert read_memory("foo") == "bar"