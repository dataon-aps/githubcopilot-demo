import pytest
import sqlite3
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch
from fastapi import status

from FastApi.models.departure import Departure


class TestGetDepartures:
    """Test suite for GET /api/departures endpoint."""

    def test_get_departures_success_with_data(self, client_with_mock_db):
        """Test successful retrieval of departures with sample data."""
        response = client_with_mock_db.get("/api/departures")
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) == 3
        
        first_departure = response.json()[0]
        assert first_departure["TrainNumber"] == "IC 342"
        assert first_departure["Origin"] == "Copenhagen"
        assert first_departure["Destination"] == "Aarhus"
        assert first_departure["Status"] == "On time"

    def test_get_departures_empty_database(self, client_with_empty_db):
        """Test retrieval when database contains no departures."""
        response = client_with_empty_db.get("/api/departures")
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0

    def test_get_departures_response_model_validation(self, client_with_mock_db):
        """Test that response data conforms to Departure model schema."""
        response = client_with_mock_db.get("/api/departures")
        data = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        
        for departure in data:
            assert "Id" in departure
            assert "TrainNumber" in departure
            assert "Origin" in departure
            assert "Destination" in departure
            assert "DepartureTime" in departure
            assert "ArrivalTime" in departure
            assert "Status" in departure
            
            assert isinstance(departure["Id"], int)
            assert isinstance(departure["TrainNumber"], str)
            assert isinstance(departure["Status"], str)

    def test_get_departures_includes_optional_fields(self, client_with_mock_db):
        """Test that optional fields (Platform, DelayMinutes) are included in response."""
        response = client_with_mock_db.get("/api/departures")
        data = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        
        first = data[0]
        assert "Platform" in first
        assert first["Platform"] == 3
        
        second = data[1]
        assert "DelayMinutes" in second
        assert second["DelayMinutes"] == 12

    def test_get_departures_database_operational_error(self, client_with_db_error):
        """Test error handling when database is unavailable."""
        response = client_with_db_error.get("/api/departures")
        
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert "Database error" in response.json()["detail"]

    def test_get_departures_integrity_error(self):
        """Test error handling when database integrity constraint is violated."""
        from FastApi import App
        from FastApi.helpers.database import get_db
        
        def override_get_db():
            db = MagicMock(spec=sqlite3.Connection)
            cursor = MagicMock()
            cursor.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
            db.cursor.return_value = cursor
            db.__enter__ = Mock(return_value=db)
            db.__exit__ = Mock(return_value=None)
            yield db
        
        App.dependency_overrides[get_db] = override_get_db
        from fastapi.testclient import TestClient
        client = TestClient(App)
        
        response = client.get("/api/departures")
        
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "conflict" in response.json()["detail"].lower()
        
        App.dependency_overrides.clear()

    def test_get_departures_generic_database_error(self):
        """Test error handling for generic SQLite errors."""
        from FastApi import App
        from FastApi.helpers.database import get_db
        
        def override_get_db():
            db = MagicMock(spec=sqlite3.Connection)
            cursor = MagicMock()
            cursor.execute.side_effect = sqlite3.DatabaseError("Generic database error")
            db.cursor.return_value = cursor
            db.__enter__ = Mock(return_value=db)
            db.__exit__ = Mock(return_value=None)
            yield db
        
        App.dependency_overrides[get_db] = override_get_db
        from fastapi.testclient import TestClient
        client = TestClient(App)
        
        response = client.get("/api/departures")
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "unexpected" in response.json()["detail"].lower()
        
        App.dependency_overrides.clear()

    def test_get_departures_unexpected_error(self):
        """Test error handling for unexpected (non-database) errors."""
        from FastApi import App
        from FastApi.helpers.database import get_db
        
        def override_get_db():
            db = MagicMock(spec=sqlite3.Connection)
            cursor = MagicMock()
            cursor.execute.side_effect = ValueError("Unexpected error")
            db.cursor.return_value = cursor
            db.__enter__ = Mock(return_value=db)
            db.__exit__ = Mock(return_value=None)
            yield db
        
        App.dependency_overrides[get_db] = override_get_db
        from fastapi.testclient import TestClient
        client = TestClient(App)
        
        response = client.get("/api/departures")
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "internal error" in response.json()["detail"].lower()
        
        App.dependency_overrides.clear()

    def test_get_departures_correct_content_type(self, client_with_mock_db):
        """Test that response has correct content type."""
        response = client_with_mock_db.get("/api/departures")
        
        assert response.status_code == status.HTTP_200_OK
        assert "application/json" in response.headers.get("content-type", "")

    def test_get_departures_delayed_train_data(self, client_with_mock_db):
        """Test that delayed train data is correctly returned."""
        response = client_with_mock_db.get("/api/departures")
        data = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        
        delayed_train = next((d for d in data if d["Status"] == "Delayed"), None)
        assert delayed_train is not None
        assert delayed_train["TrainNumber"] == "RE 1720"
        assert delayed_train["DelayMinutes"] == 12

    def test_get_departures_on_time_train_no_delay(self, client_with_mock_db):
        """Test that on-time trains have no delay minutes."""
        response = client_with_mock_db.get("/api/departures")
        data = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        
        on_time_train = next((d for d in data if d["Status"] == "On time"), None)
        assert on_time_train is not None
        assert on_time_train["DelayMinutes"] is None

    def test_get_departures_datetime_format(self, client_with_mock_db):
        """Test that datetime fields are in ISO 8601 format."""
        response = client_with_mock_db.get("/api/departures")
        data = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        
        for departure in data:
            departure_time = departure["DepartureTime"]
            arrival_time = departure["ArrivalTime"]
            
            assert isinstance(departure_time, str)
            assert isinstance(arrival_time, str)
            assert "T" in departure_time
            assert "T" in arrival_time

    def test_get_departures_consistent_field_types(self, client_with_mock_db):
        """Test that all departures have consistent field types."""
        response = client_with_mock_db.get("/api/departures")
        data = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        assert len(data) > 0
        
        for departure in data:
            assert isinstance(departure["Id"], int)
            assert isinstance(departure["TrainNumber"], str)
            assert isinstance(departure["Origin"], str)
            assert isinstance(departure["Destination"], str)
            assert isinstance(departure["Status"], str)
            assert departure["Platform"] is None or isinstance(departure["Platform"], int)
            assert departure["DelayMinutes"] is None or isinstance(departure["DelayMinutes"], int)
