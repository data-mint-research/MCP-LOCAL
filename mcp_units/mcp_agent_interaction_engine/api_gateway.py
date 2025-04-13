# 📄 Script: api_gateway.py
# 🔧 Zweck: FastAPI-Gateway für das MCP-System
# 🗂 Pfad: mcp_units/mcp_agent_interaction_engine/api_gateway.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: fastapi, uvicorn, pydantic
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Dienst implementiert die API-Gateway-Funktionalität für das MCP-System.
# HINWEIS (MCP): Er stellt Endpunkte bereit, um mit dem LangGraph zu interagieren und
# HINWEIS (MCP): Benutzeranfragen zu verarbeiten.

import time
import datetime
from typing import Dict, List, Optional, Any, Union
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import uvicorn

# Use absolute imports when running the script directly
from graph_executor import invoke_graph
from logger import log_info, log_error
from rules_api import include_rules_router
from status_api import include_status_router

# Create FastAPI application
app = FastAPI(
    title="MCP Agent Interaction Engine",
    description="API Gateway for the MCP Agent Interaction Engine",
    version="1.0.0"
)

# Include the rules and status routers
include_rules_router(app)
include_status_router(app)

# Define request and response models
class InferRequest(BaseModel):
    input: str
    policy: Dict[str, Any] = Field(default_factory=dict)

class InferResponse(BaseModel):
    output: str
    nodes_visited: List[str]
    timestamp: str
    duration_ms: int
    error: Optional[str] = None

@app.post("/mcp/infer", response_model=InferResponse)
async def infer(request: InferRequest, req: Request):
    """
    Process a user input through the LangGraph.
    
    Args:
        request: The inference request containing user input and optional policy
        
    Returns:
        The inference response with output, nodes visited, timestamp, and duration
    """
    start_time = time.time()
    client_ip = req.client.host if req.client else "unknown"
    
    # Log the incoming request
    log_info(
        "api_gateway", 
        "infer_request_received", 
        f"Received inference request from {client_ip}",
        input_length=len(request.input),
        has_policy=bool(request.policy)
    )
    
    try:
        # Invoke the graph with the user input and policy
        result = invoke_graph(request.input, request.policy)
        
        # Calculate duration in milliseconds
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Create timestamp in ISO format
        timestamp = datetime.datetime.now().isoformat() + "Z"
        
        # Extract output and nodes_visited from the result
        output = result.get("output", "")
        nodes_visited = result.get("nodes_visited", [])
        
        # Create the response
        response = InferResponse(
            output=output,
            nodes_visited=nodes_visited,
            timestamp=timestamp,
            duration_ms=duration_ms,
            error=None
        )
        
        # Log the successful response
        log_info(
            "api_gateway", 
            "infer_request_completed", 
            f"Completed inference request from {client_ip}",
            duration_ms=duration_ms,
            output_length=len(output),
            nodes_count=len(nodes_visited)
        )
        
        return response
        
    except Exception as e:
        # Calculate duration in milliseconds
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Create timestamp in ISO format
        timestamp = datetime.datetime.now().isoformat() + "Z"
        
        # Log the error
        log_error(
            "api_gateway", 
            "infer_request_failed", 
            f"Error processing inference request: {str(e)}",
            client_ip=client_ip,
            input_length=len(request.input),
            error=str(e),
            duration_ms=duration_ms
        )
        
        # Return error response with 500 status code
        error_response = InferResponse(
            output="",
            nodes_visited=[],
            timestamp=timestamp,
            duration_ms=duration_ms,
            error=str(e)
        )
        
        raise HTTPException(
            status_code=500,
            detail=error_response.dict()
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "mcp_agent_interaction_engine"}

if __name__ == "__main__":
    # Run the FastAPI application with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)