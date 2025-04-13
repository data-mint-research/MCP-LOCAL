# HINWEIS (MCP): Diese Dockerfile erstellt das Container-Image für die Agent-Interaktions-Engine.
# HINWEIS (MCP): Die Engine ist verantwortlich für die Verarbeitung des Dialogflusses und
# HINWEIS (MCP): kommuniziert mit anderen MCP-Komponenten über den Standardport 9000.
# HINWEIS (MCP): Sie ist Teil des MCP-Agent-Subsystems und verarbeitet Benutzereingaben.

FROM python:3.11-slim

# Install git
RUN apt-get update && apt-get install -y git && apt-get clean

WORKDIR /app

COPY . /app

# MCP SDK + Requirements installieren
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir git+https://github.com/modelcontextprotocol/python-sdk@main \
    && pip install --no-cache-dir fastapi uvicorn pydantic langgraph \
    && if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Standardport für MCP-Kommunikation
ENV PORT=9000

# Startbefehl ist MCP-kompatibel: wird ggf. pro Unit angepasst
CMD ["python", "api_gateway.py"]
