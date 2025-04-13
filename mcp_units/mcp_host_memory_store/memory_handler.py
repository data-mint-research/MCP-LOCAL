# 📄 Script: memory_handler.py
# 🔧 Zweck: Host-Komponente des MCP-Systems
# 🗂 Pfad: mcp_units/mcp_host_memory_store/memory_handler.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: json, os
# 🧪 Testbar: ❌

import json
import os

MEMORY = {}

MEMORY_FILE = "MCP-LOCAL/runtime_state/state_memory.json"

def write_memory(key, value):
    MEMORY[key] = value
    persist_memory()

def read_memory(key):
    return MEMORY.get(key)

def load_memory():
    global MEMORY
    if os.path.isfile(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            MEMORY = json.load(f)
    else:
        MEMORY = {}

def persist_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(MEMORY, f, indent=2)