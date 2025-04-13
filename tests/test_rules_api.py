# 📄 Script: test_rules_api.py
# 🔧 Zweck: Tests für die Rules API
# 🗂 Pfad: tests/test_rules_api.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: pytest, fastapi.testclient
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieses Skript testet die Funktionalität der Rules API,
# HINWEIS (MCP): die für die Verwaltung und Überprüfung von Regeln zuständig ist.

import os
import sys
import pytest
import yaml
from typing import Dict, Any
from fastapi.testclient import TestClient

# Add the parent directory to the Python path to import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_units.mcp_agent_interaction_engine.api_gateway import app

# Create a test client
client = TestClient(app)

def load_test_policy(policy_file: str) -> Dict[str, Any]:
    """Load a policy file for testing."""
    with open(policy_file, "r") as f:
        return yaml.safe_load(f)

def test_list_rules():
    """Test the GET /mcp/rules endpoint."""
    # Make a request to the endpoint
    response = client.get("/mcp/rules")
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that the response contains the expected fields
    data = response.json()
    assert "rules" in data
    assert "count" in data
    assert "timestamp" in data
    
    # Check that the count matches the number of rules
    assert data["count"] == len(data["rules"])
    
    # Check that each rule has the expected fields
    for rule in data["rules"]:
        assert "file_path" in rule
        assert "rule_type" in rule
        assert "content" in rule

def test_check_valid_policy():
    """Test the POST /mcp/rules/check endpoint with a valid policy."""
    # Load a known valid policy
    policy = load_test_policy("config/policies/graph.policy.yaml")
    
    # Make a request to the endpoint
    response = client.post("/mcp/rules/check", json={"policy": policy})
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that the response contains the expected fields
    data = response.json()
    assert "valid" in data
    assert "violations" in data
    assert "timestamp" in data
    assert "duration_ms" in data
    
    # Check that the policy is valid
    assert data["valid"] is True
    assert len(data["violations"]) == 0

def test_check_empty_policy():
    """Test the POST /mcp/rules/check endpoint with an empty policy."""
    # Make a request to the endpoint with an empty policy
    response = client.post("/mcp/rules/check", json={"policy": {}})
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that the response contains the expected fields
    data = response.json()
    assert "valid" in data
    assert "violations" in data
    
    # Check that the policy is invalid
    assert data["valid"] is False
    assert len(data["violations"]) > 0
    assert "Policy is empty or None" in data["violations"]

def test_check_invalid_policy():
    """Test the POST /mcp/rules/check endpoint with an invalid policy."""
    # Create an invalid policy
    policy = {
        "component": "INVALID-COMPONENT-NAME!@#",  # Invalid characters
        "enabled": True
    }
    
    # Make a request to the endpoint
    response = client.post("/mcp/rules/check", json={"policy": policy})
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that the response contains the expected fields
    data = response.json()
    assert "valid" in data
    assert "violations" in data
    
    # Check that the policy is invalid
    assert data["valid"] is False
    assert len(data["violations"]) > 0

def test_check_policy_with_specific_rules():
    """Test the POST /mcp/rules/check endpoint with specific rule files."""
    # Load a policy
    policy = load_test_policy("config/policies/graph.policy.yaml")
    
    # Make a request to the endpoint with specific rule files
    response = client.post(
        "/mcp/rules/check", 
        json={
            "policy": policy,
            "rule_files": ["config/rules/structure.rules.yaml"]
        }
    )
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that the response contains the expected fields
    data = response.json()
    assert "valid" in data
    assert "violations" in data
    
    # We don't know if the policy is valid against just the structure rules,
    # but we can check that the response is well-formed
    assert isinstance(data["valid"], bool)
    assert isinstance(data["violations"], list)

if __name__ == "__main__":
    # Run the tests
    pytest.main(["-xvs", __file__])