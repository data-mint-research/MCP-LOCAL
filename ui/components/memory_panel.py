# 📄 Script: memory_panel.py
# 🔧 Zweck: Benutzeroberfläche des MCP-Systems
# 🗂 Pfad: ui/components/memory_panel.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: Keine externen Pakete
# 🧪 Testbar: ❌

def show_memory(memory_dict):
    print("📚 Aktueller Memory-Zustand:\n")
    if not memory_dict:
        print("  (leer)")
        return
    for key, value in memory_dict.items():
        print(f"  {key}: {value}")