# 📄 Script: llm_service.py
# 🔧 Zweck: Host-Komponente des MCP-Systems
# 🗂 Pfad: mcp_units/mcp_host_llm_infer/llm_service.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: Keine externen Pakete
# 🧪 Testbar: ❌

def generate_text(prompt: str) -> str:
    if not prompt or prompt.strip() == "":
        return "Kein Prompt angegeben."
    
    # Platzhalter für LLM-Inferenz
    if "hilfe" in prompt.lower():
        return "Ich bin ein Platzhalter für ein Sprachmodell. Was brauchst du?"
    
    return f"[MOCK-LLM]: Du hast gefragt: '{prompt}'"