# 📄 Script: tool_runner.py
# 🔧 Zweck: Tool-Komponente des MCP-Systems
# 🗂 Pfad: mcp_units/mcp_tool_executor/tool_runner.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: subprocess
# 🧪 Testbar: ❌

import subprocess
import time
import sys
import os

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('tool_runner')

def run_shell_command(command):
    if not command.strip():
        return "Kein Befehl eingegeben."
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return f"Fehler:\n{e.output.strip()}"

def start_server():
    """Start the tool runner server and keep it running."""
    logger.info("Starting tool runner server...")
    logger.info(f"Process ID: {os.getpid()}")
    logger.info(f"Working directory: {os.getcwd()}")
    
    try:
        # Keep the process running
        while True:
            logger.info("Tool runner server is running...")
            time.sleep(60)  # Sleep for 60 seconds
    except KeyboardInterrupt:
        logger.info("Tool runner server shutting down...")
    except Exception as e:
        logger.error(f"Error in tool runner server: {e}")
    
    logger.info("Tool runner server stopped.")

if __name__ == "__main__":
    start_server()