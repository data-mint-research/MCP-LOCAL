from mcp_units.mcp_host_memory_store.memory_handler import write_memory, read_memory, load_memory

def test_memory_cycle():
    load_memory()
    write_memory("foo", "bar")
    assert read_memory("foo") == "bar"