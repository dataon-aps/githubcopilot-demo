# GitHub Copilot Demo - Arkitektur

## Oversigt

Denne applikation er et demonstrationsprojekt, som viser, hvordan man bygger en moderne Python-baseret API-tjeneste med FastAPI og integrerer den med en Model Context Protocol (MCP) Server til AI-funktionalitet.

## Komponenter

### 1. Code
Hovefolderen for backend-funktionaliteten.

#### 1.1 ApiApp - FastAPI Application
Et RESTful API bygget med FastAPI-frameworket til at håndtere HTTP-anmodninger og svar.

**Struktur:**
```
Code/ApiApp/
├── main.py                 # Application entry point
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
└── FastApi/
    ├── __init__.py
    ├── helpers/           # Utility modules
    │   ├── database.py    # Database connection and operations
    │   └── error_handler.py # Exception handling decorator
    ├── models/            # Pydantic data models
    │   └── departure.py   # Departure data model
    └── routers/           # API route handlers
        └── router_departure.py # Departure endpoints
```

**Hovedkomponenter:**

- **main.py**: Initialiserer FastAPI-appen, registrerer routers og starter udviklings-serveren
- **models/departure.py**: Definerer Pydantic-modeller til datavalidering af afgangsoplysninger
- **routers/router_departure.py**: Implementerer REST-endpoints til afganguoperationer
- **helpers/database.py**: Håndterer SQLite-databaseforbindelse og CRUD-operationer
- **helpers/error_handler.py**: Centraliseret fejlhåndtering med brugerdefinerede HTTP-svarmeddelelser

#### 1.2 Tests
Automatiserede tests for API'et.

**Struktur:**
```
Code/ApiApp/tests/
├── conftest.py         # Pytest fixtures og configuration
└── test_departures.py  # Tests for departure-endpoints
```

#### 1.3 McpServer
Model Context Protocol Server til integration med AI-systemer.

**Struktur:**
```
Code/McpServer/
├── server.py          # MCP server implementation
└── requirements.txt   # MCP-specifikke dependencies
```

## Dataflow

```
HTTP Request
    ↓
FastAPI Router (router_departure.py)
    ↓
Error Handler Decorator (@handle_exceptions)
    ↓
Database Helper (database.py)
    ↓
SQLite Database
    ↓
Response (via Pydantic Model)
    ↓
HTTP Response
```

## Teknologistak

- **Framework**: FastAPI (Python web framework)
- **Database**: SQLite (lokal relationsdatabase)
- **Data Validation**: Pydantic (data skema validering)
- **Testing**: Pytest (unit testing framework)
- **Integration**: Model Context Protocol (MCP) Server
- **HTTP Server**: Uvicorn (ASGI server)

## Fejlhåndtering

Applikationen bruger en centraliseret fejlhånderingsmekanisme med `@handle_exceptions`-dekoratoren, som:

1. Fanger SQLite-databasefejl og oversætter dem til passende HTTP-statuskoder
2. Logger alle fejl med funktionsnavn og fejldetaljer
3. Returnerer brugervenlige fejlmeddelelser

**Eksempel på fejlmapning:**
- `sqlite3.OperationalError` → HTTP 503 (Service Unavailable)
- `sqlite3.IntegrityError` → HTTP 409 (Conflict)
- `sqlite3.Error` → HTTP 500 (Internal Server Error)

## Deployment

Applikationen er struktureret med følgende hovedkomponenter:
- **Code/ApiApp**: Hovedtjeneste, som eksponerer HTTP-endpoints
- **Code/McpServer**: Separat tjeneste til AI-integration

## Udviklings-miljø

Se [hoveddokumentationen](../readme.md#Setting%20Up%20Your%20Development%20Environment) for instruktioner om, hvordan du opsætter et Python-miljø og installerer afhængigheder.
