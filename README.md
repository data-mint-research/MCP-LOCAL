<!-- 
📄 Datei: README.md
🔧 Zweck: Projektdokumentation und Anleitung
👤 Autor: MINT-RESEARCH
📅 Erstellt: 2025-04-13
📘 Typ: Dokumentation
-->
# MCP-LOCAL 🧠

Lokale Referenzimplementierung eines modularen, MCP-konformen Agentensystems.

## 🔧 Setup

### Voraussetzungen
- Docker (erforderlich)
  - [Windows Installation](https://docs.docker.com/desktop/install/windows-install/)
  - [macOS Installation](https://docs.docker.com/desktop/install/mac-install/)
  - [Linux Installation](https://docs.docker.com/engine/install/)
- Docker Compose (erforderlich)
  - Bereits in Docker Desktop für Windows und macOS enthalten
  - [Linux Installation](https://docs.docker.com/compose/install/linux/)
- Python 3.8+ (für lokale Entwicklung)
  - Empfohlene Python-Pakete:
    - docker
    - docker-compose

### Start und Stop

#### Starten des Systems

```bash
# Mit Docker starten (Standard)
./start.sh

# Mit Python-Prozessen starten
./start.sh --python
```

Startet alle MCP-Units je nach gewähltem Modus. Logs werden gespeichert unter:

```
# Docker-Modus
logs/docker_startup.log

# Python-Modus
logs/python_startup.log
logs/system/*.log
```

#### Stoppen des Systems

```bash
./stop.sh
```

Stoppt alle laufenden MCP-Komponenten, unabhängig davon, ob sie mit Docker oder Python gestartet wurden. Logs werden gespeichert unter:

```
logs/shutdown.log
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
> ./start.sh
> ```

---

## 📁 Verzeichnisstruktur

```text
.
├── docker-compose.yaml
├── start.sh
├── stop.sh
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

## 🐳 Docker-Konfiguration

### Installation verifizieren
```bash
# Docker-Version prüfen
docker --version

# Docker Compose-Version prüfen
docker-compose --version

# Docker-Dienst starten (nur Linux)
sudo systemctl start docker
```

### Fehlerbehebung
- **Docker nicht installiert**: Folgen Sie den Installationslinks unter Voraussetzungen
- **Docker nicht gestartet**: Starten Sie Docker Desktop (Windows/macOS) oder den Docker-Dienst (Linux)
- **Berechtigungsprobleme**: Fügen Sie Ihren Benutzer zur Docker-Gruppe hinzu (Linux)
  ```bash
  sudo usermod -aG docker $USER
  # Anmeldung erforderlich nach diesem Befehl
  ```

### Empfohlene pyproject.toml-Aktualisierung
Für die Entwicklung wird empfohlen, die folgenden Docker-bezogenen Python-Pakete in die `pyproject.toml` aufzunehmen:
```toml
dependencies = [
  "pyyaml>=6.0",
  "docker>=6.1.0",
  "docker-compose>=1.29.2"
]
```
