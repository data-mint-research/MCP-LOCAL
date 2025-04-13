<!--
📄 Datei: README.md
🔧 Zweck: Projektdokumentation und Anleitung
👤 Autor: MINT-RESEARCH
📅 Erstellt: 2025-04-13
📘 Typ: Dokumentation
-->

# MCP-LOCAL – MCP-Starterprojekt

Dieses Projekt bildet die vollständige Grundstruktur eines lauffähigen MCP-Agentensystems ab.  
Es ist modular aufgebaut und entspricht den empfohlenen MCP-Konventionen für lokale, nachvollziehbare und erweiterbare Systeme.

## Erstellt:

- `config/mcp_register.yaml` als zentrale Registry
- Projektstruktur nach MCP-Spezifikation
- Platzhalterdateien für Agent, Memory, Regeln, Policies und Logging
- Skripte zur Validierung und zum Starten des Systems

## Einstiegspunkt

Bearbeite zuerst:
`config/mcp_register.yaml`

Registriere dort alle Units in der Form:

```yaml
units:
  - id: interaction_engine
    type: mcp_agent
    path: mcp_units/mcp_agent_interaction_engine/dialog_flow.py
```

## Installation

Das Projekt kann mit pip installiert werden:

### Standardinstallation

```bash
pip install .
```

### Installation mit Entwicklungstools

```bash
pip install .[dev]
```

### Tests ausführen

```bash
pytest
```

Die Konfiguration für die Installation und Tests befindet sich in der `pyproject.toml`-Datei im Projektverzeichnis.

## Verzeichnisstruktur

```plaintext
MCP-LOCAL/
├── README.md
├── project.rules.yaml
├── pyproject.toml
│
├── config/
│   ├── mcp_register.yaml
│   ├── mcp_capabilities.yaml
│   ├── mcp_permissions.json
│   ├── rules/
│   │   ├── naming.rules.yaml
│   │   ├── structure.rules.yaml
│   │   ├── capabilities.rules.yaml
│   │   ├── agents.rules.yaml
│   │   ├── permissions.rules.yaml
│   │   └── logging.rules.yaml
│   └── policies/
│       ├── agent.policy.yaml
│       ├── memory.policy.yaml
│       └── tool.policy.yaml
│
├── runtime_state/
│   ├── state_context.json
│   ├── state_status.json
│   ├── state_memory.json
│   └── state_policy.json
│
├── logs/
│   ├── system/
│   ├── interaction/
│   ├── error/
│   ├── agent/
│   └── tool/
│
├── mcp_units/
│   ├── mcp_agent_interaction_engine/
│   │   └── dialog_flow.py
│   ├── mcp_host_memory_store/
│   │   └── memory_handler.py
│   ├── mcp_tool_executor/
│   │   └── tool_runner.py
│   └── mcp_host_llm_infer/
│       └── llm_service.py
│
├── ui/
│   ├── dashboard.py
│   └── components/
│       └── memory_panel.py
│
├── scripts/
│   ├── start_all.sh
│   ├── stop_all.sh
│   └── validate_rules.py
│
└── tests/
    ├── test_registry.py
    ├── test_status_ping.py
    ├── test_interaction.py
    ├── test_memory.py
    └── test_capabilities.py
```

## Hinweise

- `mcp_register.yaml` ist der zentrale Einstiegspunkt für alle Units.
- `rules/*.yaml` definieren die Struktur- und Verhaltensregeln.
- Policies steuern Verhalten, Memory-Ablauf und Tool-Sicherheit.
- `runtime_state/` dokumentiert den aktuellen Systemstatus.
- `scripts/` bietet Tools zur Validierung und Laufzeitsteuerung.
- Alle Tests sind auf modularen Einzelprüfungen aufgebaut.