#!/usr/bin/env python3
# 📄 Script: test_registry.py
# 🔧 Zweck: Hilfsskript für das MCP-System
# 🗂 Pfad: scripts/test_registry.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: os
# 🧪 Testbar: ❌
# HINWEIS (MCP): Dieses Skript ist ein Hilfswerkzeug für das MCP-System, das den Inhalt
# HINWEIS (MCP): der Registrierungsdatei ausgibt und die Anzahl der registrierten Einheiten zählt.
# HINWEIS (MCP): Es dient zur Überprüfung und Diagnose der MCP-Registrierung und ist Teil
# HINWEIS (MCP): des MCP-Compliance-Frameworks.

"""
Test script to print the content of the registry file
Test script to print the content of the registry file
"""

import os

# Constants
REGISTRY_FILE = "config/mcp_register.yaml"

def main():
    """
    Print the content of the registry file
    """
    print(f"Reading registry file: {REGISTRY_FILE}")
    
    try:
        with open(REGISTRY_FILE, "r") as f:
            content = f.read()
            print("Content:")
            print(content)
            
            # Count the number of units
            unit_count = content.count("  - id:")
            print(f"Found {unit_count} units in the registry")
    except Exception as e:
        print(f"Error reading registry file: {e}")

if __name__ == "__main__":
    main()