import json
import httpx
from mcp.server.fastmcp import FastMCP

API_BASE = "http://localhost:8000/api"

mcp = FastMCP(
    name="TrainTimetable",
    instructions="MCP server that queries the Train Timetable FastAPI demo app for departure data.",
)


@mcp.tool()
async def get_departures() -> str:
    """Get all train departures from the timetable API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE}/departures")
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
    except httpx.ConnectError:
        return "Error: Cannot connect to the API. Is the FastAPI app running on localhost:8000?"
    except httpx.HTTPStatusError as e:
        return f"Error: API returned status {e.response.status_code}"


@mcp.tool()
async def get_delayed_departures() -> str:
    """Get only delayed train departures (Status == 'Delayed')."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE}/departures")
            response.raise_for_status()
            departures = response.json()
            delayed = [d for d in departures if d.get("Status") == "Delayed"]
            return json.dumps(delayed, indent=2)
    except httpx.ConnectError:
        return "Error: Cannot connect to the API. Is the FastAPI app running on localhost:8000?"
    except httpx.HTTPStatusError as e:
        return f"Error: API returned status {e.response.status_code}"


@mcp.tool()
async def get_departures_by_origin(origin: str) -> str:
    """Get train departures filtered by origin station.

    Args:
        origin: The name of the origin station (e.g. 'Copenhagen', 'Aarhus').
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE}/departures")
            response.raise_for_status()
            departures = response.json()
            filtered = [d for d in departures if d.get("Origin", "").lower() == origin.lower()]
            return json.dumps(filtered, indent=2)
    except httpx.ConnectError:
        return "Error: Cannot connect to the API. Is the FastAPI app running on localhost:8000?"
    except httpx.HTTPStatusError as e:
        return f"Error: API returned status {e.response.status_code}"


if __name__ == "__main__":
    mcp.run()
