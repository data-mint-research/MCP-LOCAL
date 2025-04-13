# MCP Architecture Documentation

## Overview

The Model Context Protocol (MCP) system provides a flexible framework for managing agent interactions, policy enforcement, and rule validation. This document outlines the key architectural components and their interactions.

## System Components

### 1. Agent Interaction Engine

The Agent Interaction Engine serves as the central coordination point for all MCP operations. It manages:

- Communication between agents
- Policy enforcement
- Request routing
- Response formatting

### 2. Host LLM Inference

The Host LLM Inference component handles:

- Large language model inference requests
- Context management
- Response generation
- Model parameter configuration

### 3. Memory Store

The Memory Store provides:

- Persistent storage for conversation history
- Context retrieval for agents
- State management across sessions

### 4. Tool Executor

The Tool Executor enables:

- Dynamic tool registration and discovery
- Tool execution with appropriate permissions
- Result formatting and validation

## Rule System Architecture

### Regelprüfung zur Laufzeit (Runtime Rule Checking)

The runtime rule checking system validates that policies and operations comply with defined rules during system execution. This ensures that all components operate within their defined constraints and capabilities.

#### Components

1. **Rule Definition (`config/rules/*.rules.yaml`)**
   - YAML files defining constraints and requirements
   - Organized by domain (structure, naming, capabilities, etc.)
   - Each rule has a unique identifier and validation criteria

2. **Runtime Rule Checker (`mcp_agent_interaction_engine/runtime_rules.py`)**
   - Loads rule definitions from configuration files
   - Validates policies against rules
   - Returns detailed violation information
   - Supports both full validation and targeted rule checking

3. **Rules API (`mcp_agent_interaction_engine/rules_api.py`)**
   - Exposes rule validation through REST endpoints
   - `GET /mcp/rules` - Lists all available rules
   - `POST /mcp/rules/check` - Validates a policy against rules
   - Integrates with the main API gateway

4. **CLI Interface (`scripts/mcp_cli.py`)**
   - Provides command-line access to rule validation
   - Supports checking policies against rules
   - Formats results for human readability

#### Validation Process

1. Rules are loaded from configuration files
2. Policies are parsed and normalized
3. Each policy element is checked against applicable rules
4. Violations are collected and returned
5. Results can be accessed via API, CLI, or programmatically

#### Integration Points

- **API Gateway**: Rules API endpoints are registered with the main API gateway
- **Policy Application**: Policies are validated before being applied to the system
- **Runtime Checks**: Operations can be validated against rules during execution

## Data Flow

1. Client sends request to API Gateway
2. Request is validated against applicable rules
3. If valid, request is routed to appropriate component
4. Component processes request according to its capabilities
5. Response is formatted and returned to client

## Configuration

The system is configured through various YAML and JSON files:

- `config/mcp_register.yaml`: Component registration
- `config/mcp_capabilities.yaml`: Component capabilities
- `config/mcp_permissions.json`: Access control settings
- `config/policies/*.policy.yaml`: Operational policies
- `config/rules/*.rules.yaml`: Validation rules

## Runtime State

The system maintains runtime state in JSON files:

- `runtime_state/state_context.json`: Current context
- `runtime_state/state_memory.json`: Memory store state
- `runtime_state/state_policy.json`: Active policy
- `runtime_state/state_status.json`: System status

## Security Model

The MCP system implements a layered security model:

1. **Rule Validation**: Ensures operations comply with defined constraints
2. **Policy Enforcement**: Applies operational policies to all actions
3. **Permission Checking**: Validates access rights for operations
4. **Capability Constraints**: Limits component actions to defined capabilities

## System Monitoring

### Overview

The MCP system includes comprehensive monitoring capabilities designed to provide real-time insights into system health, component status, and operational metrics. These monitoring features serve multiple purposes:

- **Troubleshooting**: Quickly identify and diagnose issues in the system
- **Health Monitoring**: Track the operational status of all MCP components
- **Runtime Validation**: Verify that the system is operating within expected parameters
- **Operational Visibility**: Provide operators and developers with clear insights into system behavior

The monitoring architecture consists of three main components:
1. **Status API**: RESTful endpoints for programmatic access to monitoring data
2. **CLI Monitoring Commands**: Command-line interface for human-readable monitoring
3. **Docker Healthcheck**: Automated health verification for containerized services

### Status API

The Status API is implemented as part of the Agent Interaction Engine and provides HTTP endpoints for accessing real-time monitoring information. These endpoints are designed to be easily consumable by both human operators and automated monitoring systems.

#### Status Endpoint

The `/mcp/status` endpoint returns information about all registered MCP units, including their type, path, and port configuration.

**Example Request:**
```bash
curl -X GET http://localhost:9000/mcp/status
```

**Example Response:**
```json
{
  "units": [
    {
      "id": "interaction_engine",
      "type": "agent_interaction",
      "path": "mcp_units/mcp_agent_interaction_engine",
      "entry_file": "app.py",
      "port": 5000
    },
    {
      "id": "tool_executor",
      "type": "tool_execution",
      "path": "mcp_units/mcp_tool_executor",
      "entry_file": "app.py",
      "port": 5000
    }
  ],
  "count": 2,
  "timestamp": "2025-04-13T16:30:45Z"
}
```

This endpoint is particularly useful for:
- Verifying that all expected components are registered
- Checking the configuration of each component
- Monitoring the overall system composition

#### Logs Endpoint

The `/mcp/logs` endpoint retrieves log entries for a specific MCP unit, providing visibility into the operational history of that component.

**Example Request:**
```bash
curl -X GET "http://localhost:9000/mcp/logs?unit=graph_engine"
```

**Example Response:**
```json
{
  "unit": "graph_engine",
  "logs": [
    "2025-04-13T16:25:30Z - INFO - STARTUP - Graph engine initialized",
    "2025-04-13T16:26:45Z - INFO - EXECUTION - Processed graph request: graph_001",
    "2025-04-13T16:27:12Z - WARNING - PERFORMANCE - High latency detected: 1200ms"
  ],
  "count": 3,
  "timestamp": "2025-04-13T16:30:45Z"
}
```

This endpoint is valuable for:
- Diagnosing issues with specific components
- Tracking the execution flow of operations
- Identifying warning or error conditions

**Error Handling Example:**
```bash
curl -X GET "http://localhost:9000/mcp/logs?unit=nonexistent_unit"
```

**Error Response:**
```json
{
  "error": "Log file not found for unit: nonexistent_unit"
}
```

#### State Endpoint

The `/mcp/state/{bereich}` endpoint provides access to the current state of different areas of the MCP system, where `{bereich}` can be one of: `policy`, `context`, `memory`, or `status`.

**Example Requests:**
```bash
curl -X GET http://localhost:9000/mcp/state/policy
curl -X GET http://localhost:9000/mcp/state/context
curl -X GET http://localhost:9000/mcp/state/memory
```

**Example Response (policy):**
```json
{
  "policy_id": "default_policy",
  "version": "1.0.0",
  "rules": {
    "max_tokens": 4096,
    "allowed_models": ["gpt-4", "claude-2"]
  },
  "last_updated": "2025-04-13T12:00:00Z"
}
```

This endpoint enables:
- Inspecting the current system configuration
- Verifying that policies are correctly applied
- Examining the current memory and context state

### CLI Monitoring Commands

The MCP CLI provides user-friendly commands for accessing the same monitoring information available through the Status API. These commands format the data for human readability and provide additional context and explanations.

#### Status Command

The `mcp status` command displays information about all registered MCP units.

**Example:**
```bash
$ mcp status
MCP Status - 4 units registered:
  1. interaction_engine (Type: agent_interaction)
     Path: mcp_units/mcp_agent_interaction_engine
     Port: 5000

  2. tool_executor (Type: tool_execution)
     Path: mcp_units/mcp_tool_executor
     Port: 5000

  3. memory_store (Type: memory)
     Path: mcp_units/mcp_host_memory_store
     Port: 5000

  4. llm_infer (Type: inference)
     Path: mcp_units/mcp_host_llm_infer
     Port: 5000
```

This command is useful for:
- Quick system overview during development
- Verifying deployment configuration
- Troubleshooting connectivity issues

#### Logs Command

The `mcp logs --unit <unit_name>` command retrieves and displays log entries for a specific MCP unit.

**Example:**
```bash
$ mcp logs --unit graph_engine
Logs for unit 'graph_engine' - 3 entries:
  1. 2025-04-13T16:25:30Z - INFO - STARTUP - Graph engine initialized
  2. 2025-04-13T16:26:45Z - INFO - EXECUTION - Processed graph request: graph_001
  3. 2025-04-13T16:27:12Z - WARNING - PERFORMANCE - High latency detected: 1200ms
```

This command helps with:
- Real-time troubleshooting
- Monitoring component behavior
- Identifying patterns in log entries

#### State Command

The `mcp state <area>` command displays the current state for a specific area of the MCP system.

**Example:**
```bash
$ mcp state policy
State for area 'policy':
{
  "policy_id": "default_policy",
  "version": "1.0.0",
  "rules": {
    "max_tokens": 4096,
    "allowed_models": [
      "gpt-4",
      "claude-2"
    ]
  },
  "last_updated": "2025-04-13T12:00:00Z"
}
```

This command is valuable for:
- Inspecting current system configuration
- Debugging policy-related issues
- Verifying state consistency across components

### Docker Healthcheck

The MCP system includes Docker healthcheck configuration for the `mcp_gateway` service, which serves as the primary entry point for the system. This healthcheck ensures that the gateway is operational and responsive.

The healthcheck is configured in `docker-compose.yaml`:

```yaml
mcp_gateway:
  build: ./mcp_units/mcp_agent_interaction_engine
  container_name: mcp_gateway
  ports:
    - "9000:9000"
  environment:
    - PORT=9000
  command: python api_gateway.py
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:9000/mcp/status"]
    interval: 10s
    timeout: 5s
    retries: 5
```

This healthcheck:
- Runs every 10 seconds
- Tests the `/mcp/status` endpoint
- Allows 5 seconds for the endpoint to respond
- Retries up to 5 times before marking the service as unhealthy

The Docker healthcheck provides:
- Automated monitoring of service health
- Integration with Docker's service management
- Early detection of gateway failures
- Potential for automated recovery through orchestration tools

### Future Extensions

In future phases (particularly PHASE 5), the monitoring capabilities are planned to be extended to integrate with external monitoring tools and systems:

- **Metrics Export**: Integration with Prometheus for metrics collection and alerting
- **Distributed Tracing**: Implementation of OpenTelemetry for request tracing across components
- **Visualization**: Custom dashboards using Grafana or similar tools
- **Alerting**: Automated notification systems for critical issues
- **Log Aggregation**: Centralized logging with tools like ELK stack

These extensions will build upon the current monitoring architecture to provide more comprehensive observability while maintaining the same core principles of accessibility and usability for both developers and operators.

## Extensibility

The system is designed for extensibility through:

- Dynamic component registration
- Pluggable rule definitions
- Custom policy creation
- Tool registration API