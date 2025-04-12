def generate_text(prompt: str) -> str:
    if not prompt or prompt.strip() == "":
        return "Kein Prompt angegeben."
    
    # Platzhalter für LLM-Inferenz
    if "hilfe" in prompt.lower():
        return "Ich bin ein Platzhalter für ein Sprachmodell. Was brauchst du?"
    
    return f"[MOCK-LLM]: Du hast gefragt: '{prompt}'"