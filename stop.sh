#!/bin/bash
# Consolidated MCP-LOCAL shutdown script
# Replaces scripts/stop_all.sh and adds Docker shutdown

# Setup
LOG_DIR=logs
LOG_FILE=$LOG_DIR/shutdown.log
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Create log directory
mkdir -p $LOG_DIR

# Header
echo "╔════════════════════════════════════════════════╗" | tee $LOG_FILE
echo "║ MCP-LOCAL Shutdown                              ║" | tee -a $LOG_FILE
echo "║ Started: $TIMESTAMP                      ║" | tee -a $LOG_FILE
echo "╚════════════════════════════════════════════════╝" | tee -a $LOG_FILE

# Function to stop Docker containers
stop_docker() {
    echo "▶ Checking for Docker containers..." | tee -a $LOG_FILE
    
    # Check if Docker is running
    if ! docker info &> /dev/null; then
        echo "ℹ️ Docker is not running. No containers to stop." | tee -a $LOG_FILE
        return
    fi
    
    # List running containers
    RUNNING=$(docker ps --filter "name=interaction_engine|executor|memory_store|llm_infer" --format "{{.Names}}")
    
    if [ -z "$RUNNING" ]; then
        echo "ℹ️ No MCP Docker containers are running." | tee -a $LOG_FILE
        return
    fi
    
    echo "Found running MCP containers:" | tee -a $LOG_FILE
    echo "$RUNNING" | tee -a $LOG_FILE
    
    # Stop services
    echo "▶ Stopping all MCP Docker containers..." | tee -a $LOG_FILE
    docker-compose down
    
    # Verify shutdown
    STILL_RUNNING=$(docker ps --filter "name=interaction_engine|executor|memory_store|llm_infer" --format "{{.Names}}")
    
    if [ -z "$STILL_RUNNING" ]; then
        echo "✅ All MCP Docker containers have been stopped successfully." | tee -a $LOG_FILE
    else
        echo "⚠️ Some containers are still running:" | tee -a $LOG_FILE
        echo "$STILL_RUNNING" | tee -a $LOG_FILE
        echo "Attempting to force stop..." | tee -a $LOG_FILE
        
        for CONTAINER in $STILL_RUNNING; do
            echo "  Stopping $CONTAINER..." | tee -a $LOG_FILE
            docker stop $CONTAINER
        done
    fi
}

# Function to stop Python processes
stop_python() {
    echo "▶ Checking for Python processes..." | tee -a $LOG_FILE
    
    # Check if we're on Windows
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
        # Windows - use PowerShell commands
        # Find Python processes running MCP units
        PIDS=$(powershell -Command "Get-Process -Name python | Where-Object { \$_.CommandLine -like '*mcp_units*' } | Select-Object -ExpandProperty Id" 2>/dev/null)
        
        if [ -z "$PIDS" ]; then
            # Try with py command
            PIDS=$(powershell -Command "Get-Process -Name py | Where-Object { \$_.CommandLine -like '*mcp_units*' } | Select-Object -ExpandProperty Id" 2>/dev/null)
        fi
    else
        # Unix/Linux - use ps, grep, awk
        PIDS=$(ps aux | grep 'mcp_units/' | grep -v grep | awk '{print $2}')
    fi
    
    if [ -z "$PIDS" ]; then
        echo "ℹ️ No MCP Python processes are running." | tee -a $LOG_FILE
        return
    fi
    
    echo "Found running MCP processes:" | tee -a $LOG_FILE
    for PID in $PIDS; do
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
            CMD=$(powershell -Command "Get-Process -Id $PID | Select-Object -ExpandProperty CommandLine" 2>/dev/null)
        else
            CMD=$(ps -p $PID -o cmd=)
        fi
        echo "  PID $PID: $CMD" | tee -a $LOG_FILE
    done
    
    # Stop processes
    echo "▶ Stopping all MCP Python processes..." | tee -a $LOG_FILE
    for PID in $PIDS; do
        echo "✖️  Beende Prozess $PID" | tee -a $LOG_FILE
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
            powershell -Command "Stop-Process -Id $PID -Force" 2>/dev/null
        else
            kill $PID
        fi
    done
    
    # Verify all processes are stopped
    sleep 2
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
        STILL_RUNNING=$(powershell -Command "Get-Process -Name python | Where-Object { \$_.CommandLine -like '*mcp_units*' } | Select-Object -ExpandProperty Id" 2>/dev/null)
        
        if [ -z "$STILL_RUNNING" ]; then
            # Try with py command
            STILL_RUNNING=$(powershell -Command "Get-Process -Name py | Where-Object { \$_.CommandLine -like '*mcp_units*' } | Select-Object -ExpandProperty Id" 2>/dev/null)
        fi
    else
        STILL_RUNNING=$(ps aux | grep 'mcp_units/' | grep -v grep | awk '{print $2}')
    fi
    
    if [ -z "$STILL_RUNNING" ]; then
        echo "✅ All MCP Python processes have been stopped successfully." | tee -a $LOG_FILE
    else
        echo "⚠️ Some processes are still running. Attempting to force kill..." | tee -a $LOG_FILE
        for PID in $STILL_RUNNING; do
            echo "  Force killing process $PID..." | tee -a $LOG_FILE
            if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
                powershell -Command "Stop-Process -Id $PID -Force" 2>/dev/null
            else
                kill -9 $PID
            fi
        done
    fi
}

# Stop both Docker containers and Python processes
stop_docker
stop_python

echo "" | tee -a $LOG_FILE
echo "✅ MCP-LOCAL system shutdown complete." | tee -a $LOG_FILE
echo "📝 Logs saved to: $LOG_FILE" | tee -a $LOG_FILE