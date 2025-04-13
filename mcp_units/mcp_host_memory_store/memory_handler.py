# 📄 Script: memory_handler.py
# 🔧 Zweck: Host-Komponente des MCP-Systems
# 🗂 Pfad: mcp_units/mcp_host_memory_store/memory_handler.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: json, os
# 🧪 Testbar: ❌

import json
import os
import time
import sys

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('memory_handler')

MEMORY = {}

MEMORY_FILE = "runtime_state/state_memory.json"

def write_memory(key, value):
    MEMORY[key] = value
    persist_memory()

def read_memory(key):
    return MEMORY.get(key)

def load_memory():
    global MEMORY
    try:
        if os.path.isfile(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                MEMORY = json.load(f)
            logger.info(f"Memory loaded from {MEMORY_FILE}")
        else:
            MEMORY = {}
            logger.warning(f"Memory file {MEMORY_FILE} not found, initializing empty memory")
    except Exception as e:
        logger.error(f"Error loading memory: {e}")
        MEMORY = {}

def persist_memory():
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        with open(MEMORY_FILE, "w") as f:
            json.dump(MEMORY, f, indent=2)
        logger.info(f"Memory persisted to {MEMORY_FILE}")
    except Exception as e:
        logger.error(f"Error persisting memory: {e}")

def start_server():
    """Start the memory handler server and keep it running."""
    logger.info("Starting memory handler server...")
    logger.info(f"Process ID: {os.getpid()}")
    logger.info(f"Working directory: {os.getcwd()}")
    
    # Initialize memory
    load_memory()
    
    try:
        # Keep the process running
        while True:
            logger.info("Memory handler server is running...")
            time.sleep(60)  # Sleep for 60 seconds
    except KeyboardInterrupt:
        logger.info("Memory handler server shutting down...")
    except Exception as e:
        logger.error(f"Error in memory handler server: {e}")
    
    logger.info("Memory handler server stopped.")

if __name__ == "__main__":
    start_server()