# Train Timetable API Tests

Comprehensive pytest test suite for the Train Timetable FastAPI application.

## Test Coverage

### `test_departures.py`

Test suite for the `GET /api/departures` endpoint with 13 test cases covering:

#### Happy Path Tests
- `test_get_departures_success_with_data`: Successful retrieval of departures with sample data
- `test_get_departures_empty_database`: Response with empty result set
- `test_get_departures_correct_content_type`: Correct JSON content-type header

#### Response Validation Tests
- `test_get_departures_response_model_validation`: Response conforms to Departure model schema
- `test_get_departures_includes_optional_fields`: Optional fields (Platform, DelayMinutes) present
- `test_get_departures_consistent_field_types`: All departures have correct field types
- `test_get_departures_datetime_format`: DateTime fields in ISO 8601 format

#### Data-Specific Tests
- `test_get_departures_delayed_train_data`: Delayed trains correctly include delay minutes
- `test_get_departures_on_time_train_no_delay`: On-time trains have null delay minutes

#### Error Handling Tests
- `test_get_departures_database_operational_error`: Returns 503 when database is unavailable
- `test_get_departures_integrity_error`: Returns 409 for integrity constraint violations
- `test_get_departures_generic_database_error`: Returns 500 for generic SQLite errors
- `test_get_departures_unexpected_error`: Returns 500 for unexpected non-database errors

## Setup

Install test dependencies:

```bash
pip install pytest==8.0.0 pytest-asyncio==0.21.1
```

## Running Tests

Run all tests:
```bash
pytest tests/ -v
```

Run specific test class:
```bash
pytest tests/test_departures.py::TestGetDepartures -v
```

Run specific test:
```bash
pytest tests/test_departures.py::TestGetDepartures::test_get_departures_success_with_data -v
```

Run with coverage report:
```bash
pip install pytest-cov
pytest tests/ --cov=FastApi --cov-report=html
```

## Test Architecture

### Fixtures (conftest.py)

- **`mock_db`**: Generic mock SQLite connection
- **`mock_db_with_sample_data`**: Mock database with 3 sample departures
- **`client_with_mock_db`**: FastAPI TestClient with mocked database dependency
- **`client_with_empty_db`**: TestClient with empty database
- **`client_with_db_error`**: TestClient where database raises OperationalError

### Dependency Injection

Tests use FastAPI's dependency override pattern to inject mock databases:

```python
App.dependency_overrides[get_db] = override_get_db
client = TestClient(App)
# Test code here
App.dependency_overrides.clear()
```

This allows complete control over database behavior without requiring a real SQLite file.

## Project Conventions

Tests follow the Train Timetable API project guidelines:

- Use absolute imports: `from FastApi.models.departure import Departure`
- Match error handling expectations from `helpers/error_handler.py`
- Respect Pydantic v2 model configuration with `ConfigDict(populate_by_name=True)`
- Verify response schemas match `Departure` model exactly
