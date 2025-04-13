#!/bin/bash
# ──────────────────────────────────────────────────────────────
# 📄 Script: start_all.sh
# 🔧 Zweck: Startet alle registrierten MCP-Units im Hintergrund
# 🗂 Pfad: scripts/start_all.sh
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: bash, python3, nohup
# 🧪 Testbar: ✅
# ──────────────────────────────────────────────────────────────

echo "🚀 Starte alle registrierten MCP-Units..."

REGISTRY="config/mcp_register.yaml"
LOG_DIR="logs/system"

mkdir -p "$LOG_DIR"

if [ ! -f "$REGISTRY" ]; then
  echo "❌ Registry nicht gefunden: $REGISTRY"
  exit 1
fi

UNITS=$(grep "path:" "$REGISTRY" | awk '{print $2}')

for UNIT in $UNITS; do
  if [[ "$UNIT" == *.py ]]; then
    NAME=$(basename "$UNIT" .py)
    echo "▶️  Starte: $UNIT → $LOG_DIR/${NAME}.log"
    nohup python3 "$UNIT" > "$LOG_DIR/${NAME}.log" 2>&1 &
  else
    echo "⚠️  Übersprungen (kein Python-Script): $UNIT"
  fi
done

echo "✅ Alle ausführbaren Units wurden im Hintergrund gestartet."
echo "📄 Logs findest du unter: $LOG_DIR/"