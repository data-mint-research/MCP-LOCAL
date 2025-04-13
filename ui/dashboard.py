# 📄 Script: dashboard.py
# 🔧 Zweck: Benutzeroberfläche des MCP-Systems
# 🗂 Pfad: ui/dashboard.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: ui.components.memory_panel, mcp_units.mcp_host_memory_store
# 🧪 Testbar: ❌

from ui.components.memory_panel import show_memory
from mcp_units.mcp_host_memory_store import memory_handler

def main():
    memory_handler.load_memory()
    show_memory(memory_handler.MEMORY)

if __name__ == "__main__":
    print("🧠 MCP Dashboard gestartet.\n")
    main()