from ui.components.memory_panel import show_memory
from mcp_units.mcp_host_memory_store import memory_handler

def main():
    memory_handler.load_memory()
    show_memory(memory_handler.MEMORY)

if __name__ == "__main__":
    print("🧠 MCP Dashboard gestartet.\n")
    main()