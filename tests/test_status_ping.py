import json

def test_status_structure():
    with open("MCP-LOCAL/runtime_state/state_status.json") as f:
        status = json.load(f)
        assert "units" in status
        assert isinstance(status["units"], dict)