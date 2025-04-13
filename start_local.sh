#!/bin/bash

LOG_DIR=logs
LOG_FILE=$LOG_DIR/startup.log
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

mkdir -p $LOG_DIR
echo "[$TIMESTAMP] Starte MCP-LOCAL über docker-compose..." | tee $LOG_FILE

# Services definieren mit Ports
declare -A SERVICES=(
  ["interaction_engine"]="8000"
  ["executor"]="8001"
  ["memory_store"]="8002"
  ["llm_infer"]="8003"
)

# Compose starten
docker-compose up --build -d

# Wartezeit für Initialisierung
sleep 5

# Logging-Ausgabe pro Dienst
for SERVICE in "${!SERVICES[@]}"; do
  PORT=${SERVICES[$SERVICE]}
  STATUS=$(docker ps --filter "name=$SERVICE" --format "{{.Status}}")
  if [[ -n "$STATUS" ]]; then
    echo "[$(date "+%Y-%m-%d %H:%M:%S")] 🟢 $SERVICE läuft unter http://localhost:$PORT ($STATUS)" | tee -a $LOG_FILE
  else
    echo "[$(date "+%Y-%m-%d %H:%M:%S")] 🔴 $SERVICE NICHT GESTARTET!" | tee -a $LOG_FILE
  fi
done

echo "" | tee -a $LOG_FILE
echo "Fertig. Logs gespeichert unter $LOG_FILE" | tee -a $LOG_FILE
