def show_memory(memory_dict):
    print("📚 Aktueller Memory-Zustand:\n")
    if not memory_dict:
        print("  (leer)")
        return
    for key, value in memory_dict.items():
        print(f"  {key}: {value}")