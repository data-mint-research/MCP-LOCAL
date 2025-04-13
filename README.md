# MCP-LOCAL 🧠

Lokale Referenzimplementierung eines modularen, MCP-konformen Agentensystems.

## 🔧 Setup

### Voraussetzungen
- Docker
- Docker Compose
- Python (für lokale Entwicklung)

### Start (lokal)

```bash
./start_local.sh
```

Startet alle MCP-Units als Container. Logs werden gespeichert unter:

```
logs/startup.log
```

---

## 🧪 Test & Debug

| Komponente         | Port  | Testaufruf                            |
|--------------------|-------|----------------------------------------|
| `interaction_engine` | 8000 | `curl http://localhost:8000/ping`     |
| `executor`           | 8001 | `curl http://localhost:8001/status`   |
| `memory_store`       | 8002 | `curl http://localhost:8002/health`   |
| `llm_infer`          | 8003 | `curl http://localhost:8003/info`     |

> Beispiel: Status aller Dienste nach Start:
>
> ```
> ./start_local.sh
> ```

---

## 📁 Verzeichnisstruktur

```text
.
├── docker-compose.yaml
├── start_local.sh
├── logs/
│   └── startup.log
├── mcp_units/
│   ├── mcp_agent_interaction_engine/
│   ├── mcp_tool_executor/
│   ├── mcp_host_memory_store/
│   └── mcp_host_llm_infer/
├── config/
│   └── mcp_register.yaml
```

---

## 📚 Weitere Hinweise

- MCP SDK: [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- Spezifikation: [modelcontextprotocol.io](https://modelcontextprotocol.io)
