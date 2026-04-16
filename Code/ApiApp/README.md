# Train Timetable API

A simple FastAPI app that serves train departure data from a SQLite database. Used as a teaching example for GitHub Copilot workshops.

## Setup

```bash
cd FunctionApp/ApiApp
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\Activate.ps1  # Windows PowerShell

pip install -r requirements.lock
```

## Run

```bash
python main.py
```

The API starts at `http://localhost:8000`.

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/api/departures` | List all train departures |
| `GET` | `/docs` | Swagger UI (interactive API docs) |
| `GET` | `/redoc` | ReDoc (alternative API docs) |

## Example Response

```json
[
  {
    "Id": 1,
    "TrainNumber": "IC 342",
    "Origin": "Copenhagen",
    "Destination": "Aarhus",
    "DepartureTime": "2026-04-14T08:15:00",
    "ArrivalTime": "2026-04-14T11:20:00",
    "Platform": 3,
    "Status": "On time",
    "DelayMinutes": null
  }
]
```

## Project Structure

```
FunctionApp/ApiApp/
├── main.py                          ← Uvicorn entry point
├── requirements.txt                 ← Unpinned dependencies
├── requirements.lock                ← Pinned dependencies (uv pip compile)
├── FastApi/
│   ├── __init__.py                  ← App composition (router mount, CORS)
│   ├── routers/
│   │   └── router_departure.py      ← GET /api/departures
│   ├── models/
│   │   └── departure.py             ← Pydantic v2 Departure model
│   └── helpers/
│       ├── database.py              ← SQLite connection dependency + seed data
│       └── error_handler.py         ← @handle_exceptions decorator
```

The SQLite database (`timetable.db`) is created automatically on first run with sample departure data.
