#!/bin/bash
# 📄 Script: start_all.sh
# 🔧 Zweck: Hilfsskript für das MCP-System
# 🗂 Pfad: scripts/start_all.sh
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: bash
# 🧪 Testbar: ❌

echo "🚀 Starte alle registrierten MCP-Units..."

REGISTRY="config/mcp_register.yaml"

if [ ! -f "$REGISTRY" ]; then
  echo "❌ Registry nicht gefunden: $REGISTRY"
  exit 1
fi

UNITS=$(grep "path:" "$REGISTRY" | awk '{print $2}')

for UNIT in $UNITS; do
  if [[ "$UNIT" == *.py ]]; then
    echo "▶️  Starte: $UNIT"
    python3 "$UNIT" &
  else
    echo "⚠️  Übersprungen (kein Python-Script): $UNIT"
  fi
done

echo "✅ Alle ausführbaren Units wurden gestartet (Hintergrundprozesse)."