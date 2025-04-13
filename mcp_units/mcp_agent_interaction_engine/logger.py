# 📄 Script: logger.py
# 🔧 Zweck: JSON-Linien-Logger für das MCP-System
# 🗂 Pfad: mcp_units/mcp_agent_interaction_engine/logger.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: json, os, time
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Dienst implementiert einen JSON-Linien-Logger für das MCP-System.
# HINWEIS (MCP): Er schreibt strukturierte Logs im JSON-Format in Dateien im logs/system-Verzeichnis,
# HINWEIS (MCP): wobei jede Einheit ihre eigene Logdatei erhält.

import json
import os
import time
import sys
import logging
from typing import Any, Dict, Optional

# Configure standard logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('mcp_logger')

# Constants
LOG_DIR = "logs/system"

def ensure_log_directory():
    """Ensure the log directory exists."""
    os.makedirs(LOG_DIR, exist_ok=True)

def get_log_file_path(unit: str) -> str:
    """
    Get the path to the log file for the specified unit.
    
    Args:
        unit: The name of the unit (component)
        
    Returns:
        The path to the log file
    """
    return os.path.join(LOG_DIR, f"{unit}.log")

def log_event(unit: str, level: str, event: str, message: str, **kwargs) -> None:
    """
    Log an event to the appropriate log file in JSON line format.
    
    Args:
        unit: The name of the unit (component) generating the log
        level: The log level (INFO, WARNING, ERROR, DEBUG)
        event: The type of event being logged
        message: A human-readable message describing the event
        **kwargs: Additional key-value pairs to include in the log entry
    """
    try:
        # Ensure log directory exists
        ensure_log_directory()
        
        # Create log entry
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
            "unit": unit,
            "level": level.upper(),
            "event": event,
            "message": message,
            "process_id": os.getpid()
        }
        
        # Add additional fields
        log_entry.update(kwargs)
        
        # Convert to JSON
        log_json = json.dumps(log_entry)
        
        # Write to file
        log_file_path = get_log_file_path(unit)
        with open(log_file_path, "a") as f:
            f.write(log_json + "\n")
        
        # Also log to standard logger
        log_method = getattr(logger, level.lower(), logger.info)
        log_method(f"[{unit}] {event}: {message}")
        
    except Exception as e:
        # Fallback to standard logging if JSON logging fails
        logger.error(f"Error writing to log file: {e}")
        logger.error(f"Original log message: [{unit}] {level} {event}: {message}")

def log_info(unit: str, event: str, message: str, **kwargs) -> None:
    """Convenience method for logging INFO level events."""
    log_event(unit, "INFO", event, message, **kwargs)

def log_warning(unit: str, event: str, message: str, **kwargs) -> None:
    """Convenience method for logging WARNING level events."""
    log_event(unit, "WARNING", event, message, **kwargs)

def log_error(unit: str, event: str, message: str, **kwargs) -> None:
    """Convenience method for logging ERROR level events."""
    log_event(unit, "ERROR", event, message, **kwargs)

def log_debug(unit: str, event: str, message: str, **kwargs) -> None:
    """Convenience method for logging DEBUG level events."""
    log_event(unit, "DEBUG", event, message, **kwargs)