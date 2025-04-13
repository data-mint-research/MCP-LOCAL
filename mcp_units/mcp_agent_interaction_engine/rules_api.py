# 📄 Script: rules_api.py
# 🔧 Zweck: FastAPI-Endpunkte für die Verwaltung und Überprüfung von Regeln
# 🗂 Pfad: mcp_units/mcp_agent_interaction_engine/rules_api.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: fastapi, pydantic, yaml
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Dienst implementiert FastAPI-Endpunkte für die Verwaltung und Überprüfung von Regeln.
# HINWEIS (MCP): Er stellt einen /mcp/rules-Endpunkt bereit, der alle geladenen Regeln auflistet,
# HINWEIS (MCP): und einen /mcp/rules/check-Endpunkt, der eine Policy gegen die Regeln prüft.

import os
import yaml
import time
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Change from absolute imports to relative imports
from .runtime_rules import check_policy_against_rules, get_rule_files, load_rule_file
from .logger import log_event

# Create a router for the rules API
router = APIRouter()

# Define request and response models
class PolicyCheckRequest(BaseModel):
    """Request model for policy check endpoint."""
    policy: Dict[str, Any] = Field(..., description="The policy to check against rules")
    rule_files: Optional[List[str]] = Field(default=None, description="Optional list of specific rule files to check against")

class PolicyCheckResponse(BaseModel):
    """Response model for policy check endpoint."""
    valid: bool = Field(..., description="Whether the policy is valid according to the rules")
    violations: List[str] = Field(default=[], description="List of rule violations if any")
    timestamp: str = Field(..., description="Timestamp of the request")
    duration_ms: int = Field(..., description="Processing time in milliseconds")

class RuleInfo(BaseModel):
    """Model for rule information."""
    file_path: str = Field(..., description="Path to the rule file")
    rule_type: str = Field(..., description="Type of the rule (e.g., structure, naming)")
    content: Dict[str, Any] = Field(..., description="Content of the rule file")

class RulesListResponse(BaseModel):
    """Response model for rules list endpoint."""
    rules: List[RuleInfo] = Field(..., description="List of available rules")
    count: int = Field(..., description="Number of rules")
    timestamp: str = Field(..., description="Timestamp of the request")

@router.get("/mcp/rules", response_model=RulesListResponse)
async def list_rules():
    """
    List all loaded rules from the config/rules directory.
    
    Returns:
        A JSON response with the list of available rules
    """
    # Log the API request
    log_event(
        unit="rules_api",
        level="INFO",
        event="rules_list_requested",
        message="Received request to list rules"
    )
    
    try:
        # Get all rule files
        rule_files = get_rule_files()
        
        # Load each rule file and create rule info objects
        rules = []
        for file_path in rule_files:
            try:
                # Extract the rule type from the filename (e.g., "structure" from "structure.rules.yaml")
                rule_type = os.path.basename(file_path).split('.')[0]
                
                # Load the rule file
                content = load_rule_file(file_path)
                
                # Create rule info
                rule_info = RuleInfo(
                    file_path=file_path,
                    rule_type=rule_type,
                    content=content
                )
                
                rules.append(rule_info)
                
            except Exception as e:
                # Log error but continue with other rules
                log_event(
                    unit="rules_api",
                    level="ERROR",
                    event="RULE_LOAD_ERROR",
                    message=f"Error loading rule file {file_path}: {str(e)}"
                )
        
        # Create response
        response = RulesListResponse(
            rules=rules,
            count=len(rules),
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )
        
        # Log successful response
        log_event(
            unit="rules_api",
            level="INFO",
            event="rules_list_completed",
            message="Successfully listed rules",
            rule_count=len(rules)
        )
        
        return response
        
    except Exception as e:
        # Log the error
        error_message = str(e)
        log_event(
            unit="rules_api",
            level="ERROR",
            event="rules_list_failed",
            message=f"Error listing rules: {error_message}",
            error=error_message
        )
        
        # Return error response
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {error_message}"
        )

@router.post("/mcp/rules/check", response_model=PolicyCheckResponse)
async def check_policy(request: PolicyCheckRequest):
    """
    Check a policy against the defined rules.
    
    Args:
        request: The policy check request containing the policy and optional rule files
        
    Returns:
        A JSON response with the validation results
    """
    # Log the API request
    log_event(
        unit="rules_api",
        level="INFO",
        event="policy_check_requested",
        message="Received policy check request",
        policy_size=len(str(request.policy)),
        has_specific_rules=bool(request.rule_files)
    )
    
    start_time = time.time()
    
    try:
        # Check the policy against rules
        violations = check_policy_against_rules(request.policy, request.rule_files)
        
        # Calculate processing time
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Create response
        response = PolicyCheckResponse(
            valid=len(violations) == 0,
            violations=violations,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            duration_ms=duration_ms
        )
        
        # Log successful response
        log_event(
            unit="rules_api",
            level="INFO",
            event="policy_check_completed",
            message="Successfully checked policy against rules",
            valid=response.valid,
            violation_count=len(violations),
            duration_ms=duration_ms
        )
        
        return response
        
    except Exception as e:
        # Calculate processing time even for errors
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Log the error
        error_message = str(e)
        log_event(
            unit="rules_api",
            level="ERROR",
            event="policy_check_failed",
            message=f"Error checking policy against rules: {error_message}",
            error=error_message,
            duration_ms=duration_ms
        )
        
        # Return error response
        return JSONResponse(
            status_code=500,
            content={
                "valid": False,
                "violations": [f"Error during validation: {error_message}"],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "duration_ms": duration_ms
            }
        )

# Exception handlers are defined in the include_rules_router function
# to be added to the FastAPI app, not the router

# Function to include the router in the main FastAPI app
def include_rules_router(app):
    """
    Include the rules router in the main FastAPI app.
    
    Args:
        app: The FastAPI application instance
    """
    app.include_router(router)
    
    # Add exception handlers to the FastAPI app
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Custom exception handler for HTTP exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "valid": False,
                "violations": [f"Error: {exc.detail}"],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "duration_ms": 0
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """General exception handler for unexpected errors."""
        error_message = str(exc)
        log_event(
            unit="rules_api",
            level="ERROR",
            event="unhandled_exception",
            message=f"Unhandled exception: {error_message}",
            error=error_message
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "valid": False,
                "violations": [f"Internal server error: {error_message}"],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "duration_ms": 0
            }
        )