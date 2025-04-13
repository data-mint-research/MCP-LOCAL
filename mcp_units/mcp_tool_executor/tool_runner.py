# 📄 Script: tool_runner.py
# 🔧 Zweck: Tool-Komponente des MCP-Systems
# 🗂 Pfad: mcp_units/mcp_tool_executor/tool_runner.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: subprocess
# 🧪 Testbar: ❌

import subprocess

def run_shell_command(command):
    if not command.strip():
        return "Kein Befehl eingegeben."
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return f"Fehler:\n{e.output.strip()}"