from mcp_units.mcp_agent_interaction_engine.dialog_flow import handle_input

def test_handle_input():
    assert "Echo" in handle_input("Hallo")