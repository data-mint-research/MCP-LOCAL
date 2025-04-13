
FROM python:3.11-slim

# Install git
RUN apt-get update && apt-get install -y git && apt-get clean

WORKDIR /app

COPY . /app

# MCP SDK + Requirements installieren, falls vorhanden
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir git+https://github.com/modelcontextprotocol/python-sdk@main \
    && if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Standardport für MCP-Kommunikation
ENV PORT=5000

# Startbefehl ist MCP-kompatibel: wird ggf. pro Unit angepasst
CMD ["python", "memory_handler.py"]
