# 📄 Script: validate_rules.py
# 🔧 Zweck: Hilfsskript für das MCP-System
# 🗂 Pfad: scripts/validate_rules.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: os, re, yaml, json
# 🧪 Testbar: ❌
# HINWEIS (MCP): Dieses Skript ist ein wichtiges Werkzeug des MCP-Compliance-Frameworks,
# HINWEIS (MCP): das die Einhaltung der MCP-Regeln überprüft und automatisch Korrekturen vornimmt.
# HINWEIS (MCP): Es validiert und korrigiert die Struktur, Namenskonventionen, Berechtigungen und
# HINWEIS (MCP): Agentenkonfigurationen gemäß den definierten Regeln in den entsprechenden YAML-Dateien.
# HINWEIS (MCP): Das Skript stellt sicher, dass das MCP-System den Compliance-Anforderungen entspricht.

import os
import os
import re
import yaml
import json

BASE_DIR = "MCP-LOCAL"
CONFIG_DIR = os.path.join(BASE_DIR, "config")
RULES_DIR = os.path.join(CONFIG_DIR, "rules")
STATE_DIR = os.path.join(BASE_DIR, "runtime_state")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
UNITS_DIR = os.path.join(BASE_DIR, "mcp_units")

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def save_yaml(path, content):
    with open(path, "w") as f:
        yaml.dump(content, f, sort_keys=False)

def validate_and_fix_structure(structure_rules):
    print("🔍 Validierung & Korrektur: Struktur")
    actions = []
    # Units prüfen
    for t in structure_rules["mcp_units"]["required_types"]:
        if not any(d.startswith(f"mcp_{t}_") for d in os.listdir(UNITS_DIR)):
            name = f"mcp_{t}_placeholder"
            path = os.path.join(UNITS_DIR, name)
            os.makedirs(path, exist_ok=True)
            open(os.path.join(path, "main.py"), "w").close()
            actions.append(f"➕ Dummy-Unit erstellt: {name}")

    # Dateien in runtime_state prüfen
    for f in structure_rules["runtime_state"]["required_files"]:
        path = os.path.join(STATE_DIR, f)
        if not os.path.isfile(path):
            with open(path, "w") as file:
                json.dump({}, file)
            actions.append(f"➕ Datei erstellt: runtime_state/{f}")

    # Unterverzeichnisse in logs prüfen
    for sub in structure_rules["logs"]["subdirs"]:
        path = os.path.join(LOGS_DIR, sub)
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
            actions.append(f"➕ Verzeichnis erstellt: logs/{sub}")
    return actions

def validate_and_fix_naming(naming_rules):
    print("🔍 Validierung & Korrektur: Namenskonventionen")
    pattern = re.compile(naming_rules["unit_pattern"]["regex"])
    actions = []
    for d in os.listdir(UNITS_DIR):
        if not pattern.match(d):
            old_path = os.path.join(UNITS_DIR, d)
            new_name = "mcp_agent_" + d.replace("-", "_")
            new_path = os.path.join(UNITS_DIR, new_name)
            os.rename(old_path, new_path)
            actions.append(f"🔁 Umbenannt: {d} → {new_name}")
    return actions

def validate_and_fix_permissions(register_path, permissions_path):
    print("🔍 Validierung & Korrektur: Permissions")
    actions = []
    with open(register_path, "r") as f:
        units = yaml.safe_load(f).get("units", [])

    with open(permissions_path, "r") as f:
        permissions = yaml.safe_load(f)

    unit_ids = [u["id"] for u in units]
    for uid in unit_ids:
        if uid not in permissions and "default" not in permissions:
            permissions[uid] = {"access": "restricted"}
            actions.append(f"➕ Zugriff für Unit ergänzt: {uid} → restricted")

    save_yaml(permissions_path, permissions)
    return actions

def validate_and_fix_agents(agents_rules):
    print("🔍 Validierung & Korrektur: Agenten")
    actions = []
    for agent_id, agent_info in agents_rules.items():
        path = os.path.join(UNITS_DIR, agent_id)
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path, "main.py"), "w") as f:
                f.write("# Placeholder für Agent\n")
            actions.append(f"➕ Agenten-Ordner erstellt: {agent_id}")
    return actions

def main():
    structure_rules = load_yaml(os.path.join(RULES_DIR, "structure.rules.yaml"))["structure"]
    naming_rules = load_yaml(os.path.join(RULES_DIR, "naming.rules.yaml"))["naming"]
    permissions_path = os.path.join(RULES_DIR, "permissions.rules.yaml")
    agents_rules = load_yaml(os.path.join(RULES_DIR, "agents.rules.yaml"))["agents"]
    register_path = os.path.join(CONFIG_DIR, "mcp_register.yaml")

    actions = []
    actions += validate_and_fix_structure(structure_rules)
    actions += validate_and_fix_naming(naming_rules)
    actions += validate_and_fix_permissions(register_path, permissions_path)
    actions += validate_and_fix_agents(agents_rules)

    if actions:
        print("\n⚙️ Korrekturen durchgeführt:")
        for a in actions:
            print(a)
    else:
        print("\n✅ Keine Korrekturen nötig. Alles in Ordnung.")

if __name__ == "__main__":
    main()