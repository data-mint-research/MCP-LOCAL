#!/bin/bash

echo "🚀 Starte alle registrierten MCP-Units..."

REGISTRY="MCP-LOCAL/config/mcp_register.yaml"

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