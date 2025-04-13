#!/bin/bash
# Enhanced MCP-LOCAL shutdown script (PHASE 4.2)
# Supports Linux/WSL2, macOS, and Windows (via Git Bash or WSL)

# Setup
LOG_DIR="logs"
mkdir -p "$LOG_DIR"

# Parse arguments
INTERACTIVE=true
STOP_DOCKER_DESKTOP=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --stop-docker) STOP_DOCKER_DESKTOP=true ;;
        --keep-docker) STOP_DOCKER_DESKTOP=false ;;
        --non-interactive) INTERACTIVE=false; STOP_DOCKER_DESKTOP=false ;;
        --help|-h)
            echo "Usage: ./stop.sh [--stop-docker|--keep-docker] [--non-interactive]"
            echo "  --stop-docker: Stop Docker Desktop completely"
            echo "  --keep-docker: Keep Docker Desktop running (default)"
            echo "  --non-interactive: Skip all interactive prompts"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
LOG_FILE="$LOG_DIR/shutdown.log"

# Header
echo "╔════════════════════════════════════════════════╗" | tee "$LOG_FILE"
echo "║ MCP-LOCAL Enhanced Shutdown (PHASE 4.2)         ║" | tee -a "$LOG_FILE"
echo "║ Started: $TIMESTAMP                      ║" | tee -a "$LOG_FILE"
echo "╚════════════════════════════════════════════════╝" | tee -a "$LOG_FILE"

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo "▶ Detected OS: $OS" | tee -a "$LOG_FILE"

# Function to stop Tauri GUI
stop_tauri_gui() {
    echo "▶ Stopping Tauri GUI..." | tee -a "$LOG_FILE"
    
    case "$OS" in
        linux)
            # Find and kill Tauri processes
            echo "Searching for Tauri processes..." | tee -a "$LOG_FILE"
            TAURI_PIDS=$(ps aux | grep -E 'tauri|mcp-local' | grep -v grep | awk '{print $2}')
            if [ -n "$TAURI_PIDS" ]; then
                echo "Found Tauri processes: $TAURI_PIDS" | tee -a "$LOG_FILE"
                for PID in $TAURI_PIDS; do
                    echo "Stopping process $PID..." | tee -a "$LOG_FILE"
                    if kill $PID 2>/dev/null; then
                        echo "Process $PID stopped gracefully." | tee -a "$LOG_FILE"
                    elif kill -9 $PID 2>/dev/null; then
                        echo "Process $PID force stopped." | tee -a "$LOG_FILE"
                    else
                        echo "Failed to stop process $PID. It may have already exited." | tee -a "$LOG_FILE"
                    fi
                done
                echo "✅ Tauri processes stopped." | tee -a "$LOG_FILE"
            else
                echo "ℹ️ No Tauri processes found." | tee -a "$LOG_FILE"
            fi
            ;;
        macos)
            # Find and kill Tauri processes
            echo "Searching for Tauri processes..." | tee -a "$LOG_FILE"
            TAURI_PIDS=$(ps aux | grep -E 'tauri|MCP-LOCAL.app' | grep -v grep | awk '{print $2}')
            if [ -n "$TAURI_PIDS" ]; then
                echo "Found Tauri processes: $TAURI_PIDS" | tee -a "$LOG_FILE"
                for PID in $TAURI_PIDS; do
                    echo "Stopping process $PID..." | tee -a "$LOG_FILE"
                    if kill $PID 2>/dev/null; then
                        echo "Process $PID stopped gracefully." | tee -a "$LOG_FILE"
                    elif kill -9 $PID 2>/dev/null; then
                        echo "Process $PID force stopped." | tee -a "$LOG_FILE"
                    else
                        echo "Failed to stop process $PID. It may have already exited." | tee -a "$LOG_FILE"
                    fi
                done
                echo "✅ Tauri processes stopped." | tee -a "$LOG_FILE"
            else
                echo "ℹ️ No Tauri processes found." | tee -a "$LOG_FILE"
            fi
            
            # Also try to quit the app by name
            pkill -x "MCP-LOCAL" 2>/dev/null
            ;;
        windows)
            # Find and kill Tauri processes using PowerShell
            if command -v powershell.exe &> /dev/null; then
                echo "Using PowerShell to find and stop Tauri processes..." | tee -a "$LOG_FILE"
                TAURI_PIDS=$(powershell.exe -Command "Get-Process | Where-Object { \$_.Name -like '*tauri*' -or \$_.Name -like '*mcp-local*' } | Select-Object -ExpandProperty Id" 2>/dev/null)
                
                if [ -n "$TAURI_PIDS" ]; then
                    echo "Found Tauri processes: $TAURI_PIDS" | tee -a "$LOG_FILE"
                    powershell.exe -Command "Get-Process | Where-Object { \$_.Name -like '*tauri*' -or \$_.Name -like '*mcp-local*' } | Stop-Process -Force" 2>/dev/null
                    echo "✅ Tauri processes stopped." | tee -a "$LOG_FILE"
                else
                    echo "ℹ️ No Tauri processes found." | tee -a "$LOG_FILE"
                fi
            else
                # Fallback to taskkill if PowerShell is not available
                echo "Using taskkill to stop Tauri processes..." | tee -a "$LOG_FILE"
                taskkill /F /IM "mcp-local.exe" 2>/dev/null
                taskkill /F /FI "IMAGENAME eq tauri*" 2>/dev/null
            fi
            ;;
        *)
            echo "⚠️ Unsupported OS for stopping Tauri GUI." | tee -a "$LOG_FILE"
            ;;
    esac
}

# Function to stop Docker Desktop
stop_docker_desktop() {
    echo "▶ Stopping Docker Desktop..." | tee -a "$LOG_FILE"
    
    # First, stop all MCP containers
    # We're already in the root directory, so we can directly stop Docker containers
    
    # Function to stop Docker containers
    stop_docker_containers() {
        echo "▶ Checking for Docker containers..." | tee -a "$LOG_FILE"
        
        # Check if Docker is running
        if ! docker info &> /dev/null; then
            echo "ℹ️ Docker is not running. No containers to stop." | tee -a "$LOG_FILE"
            return
        fi
        
        # List running containers
        RUNNING=$(docker ps --filter "name=interaction_engine|executor|memory_store|llm_infer" --format "{{.Names}}")
        
        if [ -z "$RUNNING" ]; then
            echo "ℹ️ No MCP Docker containers are running." | tee -a "$LOG_FILE"
            return
        fi
        
        echo "Found running MCP containers:" | tee -a "$LOG_FILE"
        echo "$RUNNING" | tee -a "$LOG_FILE"
        
        # Stop services
        echo "▶ Stopping all MCP Docker containers..." | tee -a "$LOG_FILE"
        docker-compose down
        
        # Verify shutdown
        STILL_RUNNING=$(docker ps --filter "name=interaction_engine|executor|memory_store|llm_infer" --format "{{.Names}}")
        
        if [ -z "$STILL_RUNNING" ]; then
            echo "✅ All MCP Docker containers have been stopped successfully." | tee -a "$LOG_FILE"
        else
            echo "⚠️ Some containers are still running:" | tee -a "$LOG_FILE"
            echo "$STILL_RUNNING" | tee -a "$LOG_FILE"
            echo "Attempting to force stop..." | tee -a "$LOG_FILE"
            
            for CONTAINER in $STILL_RUNNING; do
                echo "  Stopping $CONTAINER..." | tee -a "$LOG_FILE"
                docker stop $CONTAINER
            done
        fi
    }
    
    # Function to stop Python processes
    stop_python_processes() {
        echo "▶ Checking for Python processes..." | tee -a "$LOG_FILE"
        
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
            echo "ℹ️ No MCP Python processes are running." | tee -a "$LOG_FILE"
            return
        fi
        
        echo "Found running MCP processes:" | tee -a "$LOG_FILE"
        for PID in $PIDS; do
            if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
                CMD=$(powershell -Command "Get-Process -Id $PID | Select-Object -ExpandProperty CommandLine" 2>/dev/null)
            else
                CMD=$(ps -p $PID -o cmd=)
            fi
            echo "  PID $PID: $CMD" | tee -a "$LOG_FILE"
        done
        
        # Stop processes
        echo "▶ Stopping all MCP Python processes..." | tee -a "$LOG_FILE"
        for PID in $PIDS; do
            echo "✖️  Beende Prozess $PID" | tee -a "$LOG_FILE"
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
            echo "✅ All MCP Python processes have been stopped successfully." | tee -a "$LOG_FILE"
        else
            echo "⚠️ Some processes are still running. Attempting to force kill..." | tee -a "$LOG_FILE"
            for PID in $STILL_RUNNING; do
                echo "  Force killing process $PID..." | tee -a "$LOG_FILE"
                if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
                    powershell -Command "Stop-Process -Id $PID -Force" 2>/dev/null
                else
                    kill -9 $PID
                fi
            done
        fi
    }
    
    # Stop both Docker containers and Python processes
    stop_docker_containers
    stop_python_processes
    
    # Check if we should stop Docker Desktop completely
    if [ "$STOP_DOCKER_DESKTOP" = true ]; then
        case "$OS" in
            linux)
                # On Linux, Docker is typically a service
                echo "▶ Stopping Docker service..." | tee -a "$LOG_FILE"
                if command -v systemctl &> /dev/null; then
                    sudo systemctl stop docker
                elif command -v service &> /dev/null; then
                    sudo service docker stop
                else
                    echo "⚠️ Could not determine how to stop Docker service." | tee -a "$LOG_FILE"
                fi
                ;;
            macos)
                # On macOS, quit Docker Desktop app
                echo "▶ Quitting Docker Desktop application..." | tee -a "$LOG_FILE"
                osascript -e 'quit app "Docker"'
                ;;
            windows)
                # On Windows, quit Docker Desktop app
                echo "▶ Quitting Docker Desktop application..." | tee -a "$LOG_FILE"
                if command -v powershell.exe &> /dev/null; then
                    powershell.exe -Command "Get-Process | Where-Object { \$_.Name -like '*Docker Desktop*' } | Stop-Process -Force" 2>/dev/null
                else
                    taskkill /F /IM "Docker Desktop.exe" 2>/dev/null
                fi
                ;;
            *)
                echo "⚠️ Unsupported OS for Docker Desktop shutdown." | tee -a "$LOG_FILE"
                ;;
        esac
    else
        echo "ℹ️ Skipping Docker Desktop shutdown as requested." | tee -a "$LOG_FILE"
    fi
}

# Ask if Docker Desktop should be stopped completely (if in interactive mode)
if [ "$INTERACTIVE" = true ] && [ "$STOP_DOCKER_DESKTOP" = false ]; then
    read -p "Do you want to stop Docker Desktop completely? (y/n): " DOCKER_CHOICE
    if [[ "$DOCKER_CHOICE" =~ ^[Yy]$ ]]; then
        STOP_DOCKER_DESKTOP=true
    fi
fi

# Log the decision
if [ "$STOP_DOCKER_DESKTOP" = true ]; then
    echo "▶ Docker Desktop will be stopped completely." | tee -a "$LOG_FILE"
else
    echo "▶ Docker Desktop will remain running." | tee -a "$LOG_FILE"
fi

# Main execution flow
stop_tauri_gui
stop_docker_desktop

echo "" | tee -a "$LOG_FILE"
echo "✅ MCP-LOCAL system shutdown complete." | tee -a "$LOG_FILE"
echo "📝 Logs saved to: $LOG_FILE" | tee -a "$LOG_FILE"