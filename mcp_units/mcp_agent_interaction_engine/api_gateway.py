# 📄 Script: api_gateway.py
# 🔧 Zweck: FastAPI-Endpunkt für das MCP-System
# 🗂 Pfad: mcp_units/mcp_agent_interaction_engine/api_gateway.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: fastapi, uvicorn
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Dienst implementiert einen FastAPI-Endpunkt für das MCP-System.
# HINWEIS (MCP): Er stellt einen /mcp/infer-Endpunkt bereit, der Benutzeranfragen entgegennimmt
# HINWEIS (MCP): und an den LangGraph weiterleitet, um Antworten zu generieren.

import time
import sys
import os
import json
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Direct imports since all files are in the same directory
from graph_executor import invoke_graph
from logger import log_event

# Configure API
app = FastAPI(
    title="MCP Agent Interaction Engine",
    description="API Gateway for the MCP Agent Interaction Engine",
    version="1.0.0"
)

# Define request and response models
class InferRequest(BaseModel):
    input: str = Field(..., description="The user input text")
    policy: Dict[str, Any] = Field(default={}, description="Optional policy configuration")

class InferResponse(BaseModel):
    output: str = Field(..., description="The generated response")
    nodes_visited: list = Field(default=[], description="List of nodes visited during processing")
    timestamp: str = Field(..., description="Timestamp of the request")
    duration_ms: int = Field(..., description="Processing time in milliseconds")
    error: Optional[str] = Field(default=None, description="Error message if an error occurred")

@app.post("/mcp/infer", response_model=InferResponse)
async def infer(request: InferRequest):
    """
    Process a user input and generate a response using the MCP system.
    
    Args:
        request: The inference request containing user input and optional policy
        
    Returns:
        A JSON response with the generated output and metadata
    """
    # Log the API request
    log_event(
        unit="api_gateway",
        level="INFO",
        event="API_REQUEST",
        message=f"Received inference request: {request.input[:50]}...",
        input_length=len(request.input),
        has_policy=bool(request.policy)
    )
    
    try:
        # Invoke the graph with the user input and policy
        result = invoke_graph(request.input, request.policy)
        
        # Log successful response
        log_event(
            unit="api_gateway",
            level="INFO",
            event="API_RESPONSE",
            message="Successfully generated response",
            duration_ms=result.get("duration_ms", 0),
            output_length=len(result.get("output", ""))
        )
        
        # Return the result
        return result
        
    except Exception as e:
        # Log the error
        error_message = str(e)
        log_event(
            unit="api_gateway",
            level="ERROR",
            event="API_ERROR",
            message=f"Error processing request: {error_message}"
        )
        
        # Return error response
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {error_message}"
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom exception handler for HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "output": f"Error: {exc.detail}",
            "nodes_visited": [],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "duration_ms": 0,
            "error": exc.detail
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler for unexpected errors."""
    error_message = str(exc)
    log_event(
        unit="api_gateway",
        level="ERROR",
        event="UNHANDLED_ERROR",
        message=f"Unhandled exception: {error_message}"
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "output": f"Internal server error: {error_message}",
            "nodes_visited": [],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "duration_ms": 0,
            "error": error_message
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

def start_server(host: str = "0.0.0.0", port: int = 9000):
    """
    Start the FastAPI server.
    
    Args:
        host: The host to bind to
        port: The port to listen on
    """
    # Check if port is already in use, if so use 9001
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.close()
    except socket.error:
        port = 9001
        print(f"Port {port-1} is already in use, using port {port} instead")
    
    # Log to both terminal and log file
    message = f"MCP Gateway running on port {port}"
    print(message)
    
    log_event(
        unit="api_gateway",
        level="INFO",
        event="SERVER_START",
        message=message
    )
    
    # Also log to dialog_flow.log for compatibility
    log_event(
        unit="dialog_flow",
        level="INFO",
        event="GATEWAY_START",
        message=message
    )
    
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()