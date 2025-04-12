import yaml

def test_registry_loads():
    with open("MCP-LOCAL/config/mcp_register.yaml") as f:
        data = yaml.safe_load(f)
        assert "units" in data