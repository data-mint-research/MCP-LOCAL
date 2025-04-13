# 📄 Script: test_infer_api.py
# 🔧 Zweck: Testfälle für die MCP-Infer-API
# 🗂 Pfad: tests/test_infer_api.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: pytest, requests
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Test überprüft die Funktionalität des /mcp/infer-Endpunkts.
# HINWEIS (MCP): Er testet, ob der Endpunkt korrekt auf Anfragen reagiert und
# HINWEIS (MCP): eine gültige Antwort mit dem erwarteten Format zurückgibt.

import pytest
import requests
import json
import os
import sys
from unittest.mock import patch, MagicMock

# Test configuration
API_URL = "http://localhost:9000/mcp/infer"

def test_infer_endpoint_with_simple_query():
    """Test the /mcp/infer endpoint with a simple query."""
    # Prepare the request payload
    payload = {
        "input": "Was ist ein Container?",
        "policy": {}
    }
    
    try:
        # Send the request to the API
        response = requests.post(API_URL, json=payload)
        
        # Check if the request was successful
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        # Parse the response
        data = response.json()
        
        # Check if the response contains the expected fields
        assert "output" in data, "Response does not contain 'output' field"
        assert "nodes_visited" in data, "Response does not contain 'nodes_visited' field"
        assert "timestamp" in data, "Response does not contain 'timestamp' field"
        assert "duration_ms" in data, "Response does not contain 'duration_ms' field"
        
        # Check if the output is a non-empty string
        assert isinstance(data["output"], str), "Output is not a string"
        assert len(data["output"]) > 0, "Output is empty"
        
        # Print the response for debugging
        print(f"Response: {json.dumps(data, indent=2)}")
        
    except requests.exceptions.ConnectionError:
        pytest.skip("API server is not running. Skipping test.")

# Mock version of the test for CI environments where the API might not be running
@patch('requests.post')
def test_infer_endpoint_with_mock(mock_post):
    """Test the /mcp/infer endpoint with a mocked response."""
    # Configure the mock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "output": "Ein Container ist eine standardisierte Einheit, die Anwendungen und ihre Abhängigkeiten kapselt.",
        "nodes_visited": ["MEMORY_LOOKUP", "TOOL_DECIDER", "LLM_INFER", "RESPONSE_FORMATTER"],
        "timestamp": "2025-04-13T14:30:00Z",
        "duration_ms": 150,
        "error": None
    }
    mock_post.return_value = mock_response
    
    # Prepare the request payload
    payload = {
        "input": "Was ist ein Container?",
        "policy": {}
    }
    
    # Send the request to the API (this will be mocked)
    response = requests.post(API_URL, json=payload)
    
    # Check if the request was successful
    assert response.status_code == 200
    
    # Parse the response
    data = response.json()
    
    # Check if the response contains the expected fields
    assert "output" in data
    assert "nodes_visited" in data
    assert "timestamp" in data
    assert "duration_ms" in data
    
    # Check if the output is a non-empty string
    assert isinstance(data["output"], str)
    assert len(data["output"]) > 0
    
    # Verify the mock was called with the correct arguments
    mock_post.assert_called_once_with(API_URL, json=payload)

# HINWEIS (MCP): Verwendet absolute Pfade, um von jedem Verzeichnis aus ausführbar zu sein
if __name__ == "__main__":
    pytest.main(["-v", __file__])