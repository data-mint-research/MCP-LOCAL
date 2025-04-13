#!/bin/bash
# Enhanced MCP-LOCAL startup script (PHASE 4.2)
# Supports Linux/WSL2, macOS, and Windows (via Git Bash or WSL)

# Default settings
TAURI_MODE="dev"
INTERACTIVE=true
LOG_DIR="logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
LOG_FILE="$LOG_DIR/startup.log"

# Header
echo "╔════════════════════════════════════════════════╗" | tee "$LOG_FILE"
echo "║ MCP-LOCAL Enhanced Startup (PHASE 4.2)          ║" | tee -a "$LOG_FILE"
echo "║ Started: $TIMESTAMP                      ║" | tee -a "$LOG_FILE"
echo "╚════════════════════════════════════════════════╝" | tee -a "$LOG_FILE"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --dev) TAURI_MODE="dev"; INTERACTIVE=false ;;
        --release) TAURI_MODE="release"; INTERACTIVE=false ;;
        --non-interactive) INTERACTIVE=false ;;
        --help|-h) 
            echo "Usage: ./start.sh [--dev|--release] [--non-interactive]"
            echo "  --dev: Start Tauri in development mode (default)"
            echo "  --release: Start Tauri in release mode"
            echo "  --non-interactive: Skip all interactive prompts"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

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

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Function to check and offer installation of required tools
check_required_tools() {
    local missing_tools=()
    
    echo "▶ Checking required tools..." | tee -a "$LOG_FILE"
    
    # Check Node.js
    if ! command_exists node; then
        echo "❌ Node.js not found" | tee -a "$LOG_FILE"
        missing_tools+=("node")
    else
        NODE_VERSION=$(node -v)
        echo "✅ Node.js found: $NODE_VERSION" | tee -a "$LOG_FILE"
    fi
    
    # Check pnpm
    if ! command_exists pnpm; then
        echo "❌ pnpm not found" | tee -a "$LOG_FILE"
        missing_tools+=("pnpm")
    else
        PNPM_VERSION=$(pnpm --version)
        echo "✅ pnpm found: $PNPM_VERSION" | tee -a "$LOG_FILE"
    fi
    
    # Check Cargo/Rust
    if ! command_exists cargo; then
        echo "❌ Cargo (Rust) not found" | tee -a "$LOG_FILE"
        missing_tools+=("cargo")
    else
        CARGO_VERSION=$(cargo --version)
        echo "✅ Cargo found: $CARGO_VERSION" | tee -a "$LOG_FILE"
    fi
    
    # Check Tauri CLI
    if ! command_exists cargo tauri; then
        echo "❌ Tauri CLI not found" | tee -a "$LOG_FILE"
        missing_tools+=("tauri")
    else
        TAURI_VERSION=$(cargo tauri --version 2>/dev/null || echo "Unknown version")
        echo "✅ Tauri CLI found: $TAURI_VERSION" | tee -a "$LOG_FILE"
    fi
    
    # Check Docker
    if ! command_exists docker; then
        echo "❌ Docker not found" | tee -a "$LOG_FILE"
        missing_tools+=("docker")
    else
        DOCKER_VERSION=$(docker --version)
        echo "✅ Docker found: $DOCKER_VERSION" | tee -a "$LOG_FILE"
    fi
    
    # Offer to install missing tools
    if [ ${#missing_tools[@]} -gt 0 ]; then
        echo "" | tee -a "$LOG_FILE"
        echo "⚠️ Missing required tools: ${missing_tools[*]}" | tee -a "$LOG_FILE"
        
        if [ "$INTERACTIVE" = true ]; then
            read -p "Would you like to install the missing tools? (y/n): " INSTALL_CHOICE
            if [[ "$INSTALL_CHOICE" =~ ^[Yy]$ ]]; then
                install_missing_tools "${missing_tools[@]}"
            else
                echo "⚠️ Continuing without installing missing tools. Some features may not work." | tee -a "$LOG_FILE"
            fi
        else
            echo "⚠️ Running in non-interactive mode. Continuing without installing missing tools." | tee -a "$LOG_FILE"
            echo "⚠️ Some features may not work properly." | tee -a "$LOG_FILE"
        fi
    else
        echo "✅ All required tools are installed." | tee -a "$LOG_FILE"
    fi
}

# Function to install missing tools
install_missing_tools() {
    local tools=("$@")
    
    for tool in "${tools[@]}"; do
        echo "▶ Installing $tool..." | tee -a "$LOG_FILE"
        
        case "$tool" in
            node)
                case "$OS" in
                    linux)
                        echo "Please run: curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs" | tee -a "$LOG_FILE"
                        ;;
                    macos)
                        echo "Please run: brew install node" | tee -a "$LOG_FILE"
                        ;;
                    windows)
                        echo "Please download and install Node.js from https://nodejs.org/" | tee -a "$LOG_FILE"
                        ;;
                esac
                ;;
            pnpm)
                echo "Installing pnpm..." | tee -a "$LOG_FILE"
                if command_exists npm; then
                    # Try to install with user permissions first
                    echo "Attempting to install pnpm with user permissions..." | tee -a "$LOG_FILE"
                    npm install -g pnpm --prefix ~/.npm-global 2>/dev/null
                    
                    # Check if installation was successful
                    if command_exists pnpm; then
                        echo "✅ pnpm installed successfully" | tee -a "$LOG_FILE"
                    else
                        # Suggest sudo installation with warning
                        echo "⚠️ Could not install pnpm with user permissions." | tee -a "$LOG_FILE"
                        echo "Please run one of the following commands:" | tee -a "$LOG_FILE"
                        echo "  sudo npm install -g pnpm" | tee -a "$LOG_FILE"
                        echo "  or" | tee -a "$LOG_FILE"
                        echo "  npm install -g pnpm --prefix ~/.npm-global && export PATH=~/.npm-global/bin:\$PATH" | tee -a "$LOG_FILE"
                    fi
                else
                    echo "❌ npm not found. Please install Node.js first." | tee -a "$LOG_FILE"
                fi
                ;;
            cargo)
                echo "Installing Rust and Cargo..." | tee -a "$LOG_FILE"
                echo "Please run: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh" | tee -a "$LOG_FILE"
                ;;
            tauri)
                echo "Installing Tauri CLI..." | tee -a "$LOG_FILE"
                if command_exists cargo; then
                    cargo install tauri-cli
                    echo "✅ Tauri CLI installed successfully" | tee -a "$LOG_FILE"
                else
                    echo "❌ Cargo not found. Please install Rust first." | tee -a "$LOG_FILE"
                fi
                ;;
            docker)
                case "$OS" in
                    linux)
                        echo "Please run: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh" | tee -a "$LOG_FILE"
                        ;;
                    macos)
                        echo "Please download and install Docker Desktop from https://www.docker.com/products/docker-desktop" | tee -a "$LOG_FILE"
                        ;;
                    windows)
                        echo "Please download and install Docker Desktop from https://www.docker.com/products/docker-desktop" | tee -a "$LOG_FILE"
                        ;;
                esac
                ;;
        esac
    done
    
    echo "⚠️ Some tools are missing. The script will continue with limited functionality." | tee -a "$LOG_FILE"
    echo "⚠️ Please install the missing tools and restart this script for full functionality." | tee -a "$LOG_FILE"
    # Continue execution instead of exiting
    sleep 3
}

# Function to start Docker Desktop
start_docker_desktop() {
    echo "▶ Starting Docker Desktop..." | tee -a "$LOG_FILE"
    
    # Check if Docker is already running
    if docker info &> /dev/null; then
        echo "✅ Docker is already running." | tee -a "$LOG_FILE"
        return 0
    fi
    
    case "$OS" in
        linux)
            # On Linux, Docker is typically a service
            echo "▶ Attempting to start Docker service..." | tee -a "$LOG_FILE"
            if command_exists systemctl; then
                sudo systemctl start docker
            elif command_exists service; then
                sudo service docker start
            else
                echo "❌ Could not determine how to start Docker service." | tee -a "$LOG_FILE"
                return 1
            fi
            ;;
        macos)
            # On macOS, start Docker Desktop app
            echo "▶ Starting Docker Desktop application..." | tee -a "$LOG_FILE"
            open -a Docker
            ;;
        windows)
            # On Windows, start Docker Desktop app
            echo "▶ Starting Docker Desktop application..." | tee -a "$LOG_FILE"
            if command_exists powershell.exe; then
                powershell.exe -Command "Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe'"
            else
                start "C:\Program Files\Docker\Docker\Docker Desktop.exe"
            fi
            ;;
        *)
            echo "❌ Unsupported OS for Docker Desktop startup." | tee -a "$LOG_FILE"
            return 1
            ;;
    esac
    
    # Wait for Docker to start
    echo "▶ Waiting for Docker to start..." | tee -a "$LOG_FILE"
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker info &> /dev/null; then
            echo "✅ Docker started successfully after $attempt attempts." | tee -a "$LOG_FILE"
            return 0
        fi
        echo "⏳ Waiting for Docker to start (attempt $attempt/$max_attempts)..." | tee -a "$LOG_FILE"
        sleep 2
        ((attempt++))
    done
    
    echo "❌ Failed to start Docker after $max_attempts attempts." | tee -a "$LOG_FILE"
    return 1
}

# Function to start Tauri GUI
start_tauri_gui() {
    local mode=$1
    
    echo "▶ Starting Tauri GUI in $mode mode..." | tee -a "$LOG_FILE"
    # Navigate to the UI directory
    # The UI directory is at the root level of the project
    cd ui || {
        echo "❌ UI directory not found at ui" | tee -a "$LOG_FILE"
        # Try alternative path
        cd $(dirname "$0")/ui || {
            echo "❌ UI directory not found at alternative path" | tee -a "$LOG_FILE"
            return 1
        }
    }
    
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "▶ Installing dependencies..." | tee -a "../$LOG_FILE"
        if command_exists pnpm; then
            pnpm install
        else
            echo "⚠️ pnpm not found. Attempting to use npm instead..." | tee -a "../$LOG_FILE"
            npm install
        fi
    fi
    
    # Start Tauri
    if [ "$mode" = "dev" ]; then
        echo "▶ Starting Tauri in development mode..." | tee -a "../$LOG_FILE"
        if command_exists pnpm; then
            pnpm tauri dev &
        elif command_exists npm; then
            npm run tauri dev &
        else
            echo "❌ Neither pnpm nor npm is available. Cannot start Tauri in dev mode." | tee -a "../$LOG_FILE"
            return 1
        fi
    else
        echo "▶ Building and starting Tauri in release mode..." | tee -a "../$LOG_FILE"
        if command_exists pnpm; then
            pnpm tauri build
        elif command_exists npm; then
            npm run tauri build
        else
            echo "❌ Neither pnpm nor npm is available. Cannot build Tauri." | tee -a "../$LOG_FILE"
            return 1
        fi
        
        # Start the built application
        case "$OS" in
            linux)
                echo "▶ Starting built Tauri application..." | tee -a "../$LOG_FILE"
                # Path may need adjustment based on your project
                ./src-tauri/target/release/mcp-local &
                ;;
            macos)
                echo "▶ Starting built Tauri application..." | tee -a "../$LOG_FILE"
                open ./src-tauri/target/release/bundle/macos/MCP-LOCAL.app
                ;;
            windows)
                echo "▶ Starting built Tauri application..." | tee -a "../$LOG_FILE"
                start ./src-tauri/target/release/mcp-local.exe
                ;;
            *)
                echo "❌ Unsupported OS for starting built Tauri application." | tee -a "../$LOG_FILE"
                return 1
                ;;
        esac
    fi
    
    # Return to the original directory
    cd - > /dev/null
    
    echo "✅ Tauri GUI started in $mode mode." | tee -a "$LOG_FILE"
}

# Function to start MCP services
start_mcp_services() {
    echo "▶ Starting MCP services..." | tee -a "$LOG_FILE"
    
    # We're already in the root directory, so no need to navigate
    # Just execute the Docker or Python startup based on the mode
    
    # Default mode
    MODE="docker"
    
    # Parse arguments
    while [[ "$#" -gt 0 ]]; do
        case $1 in
            --docker) MODE="docker" ;;
            --python) MODE="python" ;;
            *) break ;;
        esac
        shift
    done
    
    if [ "$MODE" = "docker" ]; then
        # Start Docker mode
        LOG_FILE_MCP="$LOG_DIR/docker_startup.log"
        echo "Starting MCP services in Docker mode..." | tee -a "$LOG_FILE"
        
        # Check Docker
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker not found. Please install Docker and try again." | tee -a "$LOG_FILE"
            return 1
        fi
        
        # Check Docker Compose
        if ! command -v docker-compose &> /dev/null; then
            echo "❌ Docker Compose not found. Please install Docker Compose and try again." | tee -a "$LOG_FILE"
            return 1
        fi
        
        # Check if Docker is running
        if ! docker info &> /dev/null; then
            echo "❌ Docker is not running. Please start Docker and try again." | tee -a "$LOG_FILE"
            return 1
        fi
        
        # Services
        declare -A SERVICES=(
          ["interaction_engine"]="8000"
          ["executor"]="8001"
          ["memory_store"]="8002"
          ["llm_infer"]="8003"
          ["mcp_gateway"]="9000"
        )
        
        # Start services
        echo "▶ Starting Docker containers..." | tee -a "$LOG_FILE"
        docker-compose up --build -d
        
        # Wait for initialization
        echo "▶ Waiting for services to initialize..." | tee -a "$LOG_FILE"
        sleep 5
        
        # Check services
        echo "▶ Checking service status..." | tee -a "$LOG_FILE"
        ALL_RUNNING=true
        
        for SERVICE in "${!SERVICES[@]}"; do
          PORT=${SERVICES[$SERVICE]}
          STATUS=$(docker ps --filter "name=$SERVICE" --format "{{.Status}}")
          
          if [[ -n "$STATUS" ]]; then
            echo "[$(date "+%Y-%m-%d %H:%M:%S")] 🟢 $SERVICE läuft unter http://localhost:$PORT ($STATUS)" | tee -a "$LOG_FILE"
          else
            echo "[$(date "+%Y-%m-%d %H:%M:%S")] 🔴 $SERVICE NICHT GESTARTET!" | tee -a "$LOG_FILE"
            ALL_RUNNING=false
          fi
        done
        
        # Summary
        echo "" | tee -a "$LOG_FILE"
        if [ "$ALL_RUNNING" = true ]; then
          echo "✅ Alle Docker-Dienste wurden erfolgreich gestartet." | tee -a "$LOG_FILE"
        else
          echo "⚠️ Einige Docker-Dienste konnten nicht gestartet werden. Prüfe die Logs für Details." | tee -a "$LOG_FILE"
        fi
    elif [ "$MODE" = "python" ]; then
        # Start Python mode
        LOG_FILE_MCP="$LOG_DIR/python_startup.log"
        SYSTEM_LOG_DIR="$LOG_DIR/system"
        mkdir -p "$SYSTEM_LOG_DIR"
        
        echo "Starting MCP services in Python mode..." | tee -a "$LOG_FILE"
        
        # Check Python
        if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null && ! command -v py &> /dev/null; then
            echo "❌ Python not found. Please install Python and try again." | tee -a "$LOG_FILE"
            return 1
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
            echo "❌ Registry nicht gefunden: $REGISTRY" | tee -a "$LOG_FILE"
            return 1
        fi
        
        echo "🚀 Starte alle registrierten MCP-Units..." | tee -a "$LOG_FILE"
        
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
                echo "▶️  Starte: $UNIT → $SYSTEM_LOG_DIR/${NAME}.log" | tee -a "$LOG_FILE"
                nohup $PYTHON_CMD "$UNIT" > "$SYSTEM_LOG_DIR/${NAME}.log" 2>&1 &
            else
                echo "⚠️  Übersprungen (kein Python-Script): $UNIT" | tee -a "$LOG_FILE"
            fi
        done
        
        echo "✅ Alle ausführbaren Units wurden im Hintergrund gestartet." | tee -a "$LOG_FILE"
        echo "📄 Logs findest du unter: $SYSTEM_LOG_DIR/" | tee -a "$LOG_FILE"
    else
        echo "❌ Unknown mode: $MODE" | tee -a "$LOG_FILE"
        return 1
    fi
    
    echo "✅ MCP services started." | tee -a "$LOG_FILE"
}

# Main execution flow
check_required_tools

# Start Docker Desktop
start_docker_desktop

# Start MCP services
start_mcp_services --docker

# Determine Tauri mode if interactive
if [ "$INTERACTIVE" = true ] && [ "$TAURI_MODE" = "dev" ]; then
    echo "" | tee -a "$LOG_FILE"
    echo "Please select Tauri GUI mode:" | tee -a "$LOG_FILE"
    echo "1) Development mode (faster startup, live reloading)" | tee -a "$LOG_FILE"
    echo "2) Release mode (optimized build)" | tee -a "$LOG_FILE"
    read -p "Enter your choice [1-2]: " TAURI_CHOICE
    
    case "$TAURI_CHOICE" in
        2) TAURI_MODE="release" ;;
        *) TAURI_MODE="dev" ;;
    esac
fi

# Start Tauri GUI
start_tauri_gui "$TAURI_MODE"

echo "" | tee -a "$LOG_FILE"
echo "✅ MCP-LOCAL system started successfully." | tee -a "$LOG_FILE"
echo "📝 Logs saved to: $LOG_FILE" | tee -a "$LOG_FILE"
echo "ℹ️ Use './stop.sh' to stop the system." | tee -a "$LOG_FILE"