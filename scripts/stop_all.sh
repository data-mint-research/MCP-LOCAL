#!/bin/bash
# 📄 Script: stop_all.sh
# 🔧 Zweck: Hilfsskript für das MCP-System
# 🗂 Pfad: scripts/stop_all.sh
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: bash
# 🧪 Testbar: ❌

echo "🛑 Stoppe alle laufenden MCP-Units..."

# Nur testweise über Prozessname
PIDS=$(ps aux | grep 'mcp_units/' | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
  echo "ℹ️  Keine laufenden Prozesse gefunden."
  exit 0
fi

for PID in $PIDS; do
  echo "✖️  Beende Prozess $PID"
  kill $PID
done

echo "✅ Alle bekannten MCP-Unit-Prozesse wurden beendet."