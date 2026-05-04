---
name: train-timetable-usage
description: Use the Train Timetable MCP server to query live departure data from the FastAPI demo app during Copilot Chat conversations. The MCP server wraps the `/api/departures` endpoint and exposes it as tools that Copilot can call in Agent mode.
---

# Skill: Train Timetable MCP Server

## Description

## Prerequisites

1. The FastAPI app must be running locally on `http://localhost:8000`
2. The MCP server must be configured in `.vscode/mcp.json`
3. Install dependencies: `pip install -r FunctionApp/McpServer/requirements.txt`

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_departures` | Fetch all departures from the timetable | None |
| `get_delayed_departures` | Fetch only delayed departures | None |
| `get_departures_by_origin` | Fetch departures filtered by origin station | `origin` (str) — station name |

## Usage Examples

In Copilot Chat (Agent mode), you can ask:

- *"Get all train departures from the timetable"*
- *"Which trains are currently delayed?"*
- *"Show me all departures from Copenhagen"*
- *"Are there any cancelled trains?"* (use `get_departures` and analyse the results)

## How to Start

1. Start the FastAPI app:
   ```bash
   cd FunctionApp/ApiApp
   python main.py
   ```

2. The MCP server starts automatically when Copilot invokes a tool (configured via `mcp.json`).

## Architecture

```
Copilot Agent ──▶ MCP Server (server.py) ──▶ FastAPI App (localhost:8000)
                  Uses httpx to call            Reads from SQLite DB
                  /api/departures
```

The MCP server is a thin wrapper — it calls the existing REST API and returns the results as structured JSON that Copilot can reason about.
