# 📄 Script: status_api.py
# 🔧 Zweck: FastAPI-Endpunkte für Statusabfragen des MCP-Systems
# 🗂 Pfad: mcp_units/mcp_agent_interaction_engine/status_api.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: fastapi, pydantic, yaml, json, os
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Dienst implementiert FastAPI-Endpunkte für Statusabfragen des MCP-Systems.
# HINWEIS (MCP): Er stellt Endpunkte bereit, um registrierte Einheiten, Logs und Zustandsdaten abzurufen.

import os
import json
import yaml
import time
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Use absolute imports when running the script directly
from logger import log_event

# Constants
CONFIG_DIR = "config"
LOGS_DIR = "logs/system"
RUNTIME_STATE_DIR = "runtime_state"
MCP_REGISTER_FILE = os.path.join(CONFIG_DIR, "mcp_register.yaml")
MAX_LOG_LINES = 50

# Create a router for the status API
router = APIRouter()

# Define response models
class UnitInfo(BaseModel):
    """Model for unit information."""
    id: str = Field(..., description="Unit ID")
    type: str = Field(..., description="Unit type")
    path: str = Field(..., description="Path to the unit implementation")
    entry_file: str = Field(..., description="Entry file for the unit")
    port: Optional[int] = Field(None, description="Port number (if applicable)")

class StatusResponse(BaseModel):
    """Response model for status endpoint."""
    units: List[UnitInfo] = Field(..., description="List of registered units")
    count: int = Field(..., description="Number of units")
    timestamp: str = Field(..., description="Timestamp of the request")

class LogsResponse(BaseModel):
    """Response model for logs endpoint."""
    unit: str = Field(..., description="Unit name")
    logs: List[str] = Field(..., description="Log entries")
    count: int = Field(..., description="Number of log entries")
    timestamp: str = Field(..., description="Timestamp of the request")

@router.get("/mcp/status", response_model=StatusResponse)
async def get_status():
    """
    Get the status of all registered MCP units.
    
    Returns:
        A JSON response with the list of registered units
    """
    # Log the API request
    log_event(
        unit="status_api",
        level="INFO",
        event="API_REQUEST",
        message="Received request to get MCP status"
    )
    
    try:
        # Load the MCP register file
        if not os.path.exists(MCP_REGISTER_FILE):
            log_event(
                unit="status_api",
                level="ERROR",
                event="FILE_NOT_FOUND",
                message=f"MCP register file not found: {MCP_REGISTER_FILE}"
            )
            raise HTTPException(
                status_code=404,
                detail=f"MCP register file not found: {MCP_REGISTER_FILE}"
            )
        
        with open(MCP_REGISTER_FILE, "r") as f:
            register_data = yaml.safe_load(f)
        
        # Extract unit information
        units = []
        for unit_data in register_data.get("units", []):
            unit = UnitInfo(
                id=unit_data.get("id", ""),
                type=unit_data.get("type", ""),
                path=unit_data.get("path", ""),
                entry_file=unit_data.get("entry_file", ""),
                port=unit_data.get("port")
            )
            units.append(unit)
        
        # Create response
        response = StatusResponse(
            units=units,
            count=len(units),
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )
        
        # Log successful response
        log_event(
            unit="status_api",
            level="INFO",
            event="API_RESPONSE",
            message="Successfully retrieved MCP status",
            unit_count=len(units)
        )
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error
        error_message = str(e)
        log_event(
            unit="status_api",
            level="ERROR",
            event="API_ERROR",
            message=f"Error retrieving MCP status: {error_message}"
        )
        
        # Return error response
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {error_message}"}
        )

@router.get("/mcp/logs")
async def get_logs(unit: str):
    """
    Get the logs for a specific MCP unit.
    
    Args:
        unit: The name of the unit to get logs for
        
    Returns:
        A JSON response with the log entries
    """
    # Log the API request
    log_event(
        unit="status_api",
        level="INFO",
        event="API_REQUEST",
        message=f"Received request to get logs for unit: {unit}"
    )
    
    try:
        # Construct the log file path
        log_file_path = os.path.join(LOGS_DIR, f"{unit}.log")
        
        # Check if the log file exists
        if not os.path.exists(log_file_path):
            log_event(
                unit="status_api",
                level="ERROR",
                event="FILE_NOT_FOUND",
                message=f"Log file not found for unit: {unit}"
            )
            return JSONResponse(
                status_code=404,
                content={"error": f"Log file not found for unit: {unit}"}
            )
        
        # Read the log file (last MAX_LOG_LINES lines)
        logs = []
        with open(log_file_path, "r") as f:
            # Read all lines and keep only the last MAX_LOG_LINES
            all_lines = f.readlines()
            logs = all_lines[-MAX_LOG_LINES:] if len(all_lines) > MAX_LOG_LINES else all_lines
            
            # Strip newlines
            logs = [line.strip() for line in logs]
        
        # Create response
        response = {
            "unit": unit,
            "logs": logs,
            "count": len(logs),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        
        # Log successful response
        log_event(
            unit="status_api",
            level="INFO",
            event="API_RESPONSE",
            message=f"Successfully retrieved logs for unit: {unit}",
            log_count=len(logs)
        )
        
        return response
        
    except Exception as e:
        # Log the error
        error_message = str(e)
        log_event(
            unit="status_api",
            level="ERROR",
            event="API_ERROR",
            message=f"Error retrieving logs for unit {unit}: {error_message}"
        )
        
        # Return error response
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {error_message}"}
        )

@router.get("/mcp/state/{bereich}")
async def get_state(bereich: str):
    """
    Get the state for a specific area of the MCP system.
    
    Args:
        bereich: The area to get state for (e.g., policy, context, memory)
        
    Returns:
        A JSON response with the state data
    """
    # Log the API request
    log_event(
        unit="status_api",
        level="INFO",
        event="API_REQUEST",
        message=f"Received request to get state for area: {bereich}"
    )
    
    try:
        # Construct the state file path
        state_file_path = os.path.join(RUNTIME_STATE_DIR, f"state_{bereich}.json")
        
        # Check if the state file exists
        if not os.path.exists(state_file_path):
            log_event(
                unit="status_api",
                level="ERROR",
                event="FILE_NOT_FOUND",
                message=f"State file not found for area: {bereich}"
            )
            return JSONResponse(
                status_code=404,
                content={"error": f"State file not found for area: {bereich}"}
            )
        
        # Read the state file
        with open(state_file_path, "r") as f:
            state_data = json.load(f)
        
        # Log successful response
        log_event(
            unit="status_api",
            level="INFO",
            event="API_RESPONSE",
            message=f"Successfully retrieved state for area: {bereich}",
            data_size=len(json.dumps(state_data))
        )
        
        return state_data
        
    except json.JSONDecodeError as e:
        # Log the error
        error_message = f"Invalid JSON in state file: {str(e)}"
        log_event(
            unit="status_api",
            level="ERROR",
            event="JSON_ERROR",
            message=error_message,
            file_path=state_file_path
        )
        
        # Return error response
        return JSONResponse(
            status_code=500,
            content={"error": error_message}
        )
    except Exception as e:
        # Log the error
        error_message = str(e)
        log_event(
            unit="status_api",
            level="ERROR",
            event="API_ERROR",
            message=f"Error retrieving state for area {bereich}: {error_message}"
        )
        
        # Return error response
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {error_message}"}
        )

# Function to include the status router in the main FastAPI app
def include_status_router(app):
    """
    Include the status router in the main FastAPI app.
    
    Args:
        app: The FastAPI application instance
    """
    app.include_router(router)