#!/bin/bash
# Consolidated MCP-LOCAL startup script
# Replaces start_local.sh and scripts/start_all.sh

# Default mode
MODE="docker"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --docker) MODE="docker" ;;
        --python) MODE="python" ;;
        --help|-h) 
            echo "Usage: ./start.sh [--docker|--python]"
            echo "  --docker: Start using Docker containers (default)"
            echo "  --python: Start using Python processes"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Setup
LOG_DIR=logs
mkdir -p $LOG_DIR
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Header
echo "╔════════════════════════════════════════════════╗"
echo "║ MCP-LOCAL Startup                               ║"
echo "║ Mode: $MODE                                     ║"
echo "║ Started: $TIMESTAMP                      ║"
echo "╚════════════════════════════════════════════════╝"

# Function to start Docker mode
start_docker_mode() {
    LOG_FILE=$LOG_DIR/docker_startup.log
    echo "Starting in Docker mode..." | tee $LOG_FILE
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Please install Docker and try again." | tee -a $LOG_FILE
        exit 1
    fi

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose not found. Please install Docker Compose and try again." | tee -a $LOG_FILE
        exit 1
    fi

    # Check if Docker is running
    if ! docker info &> /dev/null; then
        echo "❌ Docker is not running. Please start Docker and try again." | tee -a $LOG_FILE
        exit 1
    fi

    # Services
    declare -A SERVICES=(
      ["interaction_engine"]="8000"
      ["executor"]="8001"
      ["memory_store"]="8002"
      ["llm_infer"]="8003"
    )

    # Start services
    echo "▶ Starting Docker containers..." | tee -a $LOG_FILE
    docker-compose up --build -d

    # Wait for initialization
    echo "▶ Waiting for services to initialize..." | tee -a $LOG_FILE
    sleep 5

    # Check services
    echo "▶ Checking service status..." | tee -a $LOG_FILE
    ALL_RUNNING=true

    for SERVICE in "${!SERVICES[@]}"; do
      PORT=${SERVICES[$SERVICE]}
      STATUS=$(docker ps --filter "name=$SERVICE" --format "{{.Status}}")
      
      if [[ -n "$STATUS" ]]; then
        echo "[$(date "+%Y-%m-%d %H:%M:%S")] 🟢 $SERVICE läuft unter http://localhost:$PORT ($STATUS)" | tee -a $LOG_FILE
      else
        echo "[$(date "+%Y-%m-%d %H:%M:%S")] 🔴 $SERVICE NICHT GESTARTET!" | tee -a $LOG_FILE
        ALL_RUNNING=false
      fi
    done

    # Summary
    echo "" | tee -a $LOG_FILE
    if [ "$ALL_RUNNING" = true ]; then
      echo "✅ Alle Docker-Dienste wurden erfolgreich gestartet." | tee -a $LOG_FILE
    else
      echo "⚠️ Einige Docker-Dienste konnten nicht gestartet werden. Prüfe die Logs für Details." | tee -a $LOG_FILE
    fi

    echo "📝 Logs gespeichert unter: $LOG_FILE" | tee -a $LOG_FILE
}

# Function to start Python mode
start_python_mode() {
    LOG_FILE=$LOG_DIR/python_startup.log
    SYSTEM_LOG_DIR="$LOG_DIR/system"
    mkdir -p "$SYSTEM_LOG_DIR"
    
    echo "Starting in Python mode..." | tee $LOG_FILE
    
    # Check Python
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null && ! command -v py &> /dev/null; then
        echo "❌ Python not found. Please install Python and try again." | tee -a $LOG_FILE
        exit 1
    fi
    
    # Determine Python command
    PYTHON_CMD="python3"
    if ! command -v python3 &> /dev/null; then
        if command -v python &> /dev/null; then
            PYTHON_CMD="python"
        elif command -v py &> /dev/null; then
            PYTHON_CMD="py"
        fi
    fi
    
    # Check registry file
    REGISTRY="config/mcp_register.yaml"
    if [ ! -f "$REGISTRY" ]; then
        echo "❌ Registry nicht gefunden: $REGISTRY" | tee -a $LOG_FILE
        exit 1
    fi
    
    echo "🚀 Starte alle registrierten MCP-Units..." | tee -a $LOG_FILE
    
    # Extract units from registry
    UNITS=$($PYTHON_CMD -c "
import yaml
with open('$REGISTRY', 'r') as f:
    data = yaml.safe_load(f)
    if data and 'units' in data:
        for unit in data['units']:
            if 'path' in unit:
                print(unit['path'])
    ")
    
    # Start each unit
    for UNIT in $UNITS; do
        if [[ "$UNIT" == *.py ]]; then
            NAME=$(basename "$UNIT" .py)
            echo "▶️  Starte: $UNIT → $SYSTEM_LOG_DIR/${NAME}.log" | tee -a $LOG_FILE
            nohup $PYTHON_CMD "$UNIT" > "$SYSTEM_LOG_DIR/${NAME}.log" 2>&1 &
        else
            echo "⚠️  Übersprungen (kein Python-Script): $UNIT" | tee -a $LOG_FILE
        fi
    done
    
    echo "✅ Alle ausführbaren Units wurden im Hintergrund gestartet." | tee -a $LOG_FILE
    echo "📄 Logs findest du unter: $SYSTEM_LOG_DIR/" | tee -a $LOG_FILE
}

# Start in the selected mode
if [ "$MODE" = "docker" ]; then
    start_docker_mode
elif [ "$MODE" = "python" ]; then
    start_python_mode
else
    echo "❌ Unknown mode: $MODE"
    exit 1
fi

echo ""
echo "MCP-LOCAL system started in $MODE mode."
echo "Use './stop.sh' to stop the system."