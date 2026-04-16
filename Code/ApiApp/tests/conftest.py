import pytest
import sqlite3
from datetime import datetime
from unittest.mock import Mock, MagicMock
from fastapi.testclient import TestClient

from FastApi import App
from FastApi.helpers.database import get_db


@pytest.fixture
def mock_db():
    """Create a mock SQLite connection for testing."""
    db = MagicMock(spec=sqlite3.Connection)
    db.cursor.return_value = MagicMock()
    return db


@pytest.fixture
def mock_db_with_sample_data():
    """Create a mock database with sample departure data."""
    db = MagicMock(spec=sqlite3.Connection)
    cursor = MagicMock()
    
    sample_data = [
        (1, "IC 342", "Copenhagen", "Aarhus", "2026-04-14T08:15:00", "2026-04-14T11:20:00", 3, "On time", None),
        (2, "RE 1720", "Odense", "Copenhagen", "2026-04-14T09:00:00", "2026-04-14T10:32:00", 7, "Delayed", 12),
        (3, "IC 855", "Aarhus", "Aalborg", "2026-04-14T10:45:00", "2026-04-14T12:10:00", 1, "On time", None),
    ]
    
    cursor.description = [
        ('Id',), ('TrainNumber',), ('Origin',), ('Destination',),
        ('DepartureTime',), ('ArrivalTime',), ('Platform',), ('Status',), ('DelayMinutes',)
    ]
    cursor.fetchall.return_value = sample_data
    db.cursor.return_value = cursor
    db.__enter__ = Mock(return_value=db)
    db.__exit__ = Mock(return_value=None)
    
    return db


@pytest.fixture
def client_with_mock_db(mock_db_with_sample_data):
    """Create a TestClient with a mocked database dependency."""
    def override_get_db():
        yield mock_db_with_sample_data
    
    App.dependency_overrides[get_db] = override_get_db
    client = TestClient(App)
    
    yield client
    
    App.dependency_overrides.clear()


@pytest.fixture
def client_with_empty_db():
    """Create a TestClient with an empty database."""
    db = MagicMock(spec=sqlite3.Connection)
    cursor = MagicMock()
    
    cursor.description = [
        ('Id',), ('TrainNumber',), ('Origin',), ('Destination',),
        ('DepartureTime',), ('ArrivalTime',), ('Platform',), ('Status',), ('DelayMinutes',)
    ]
    cursor.fetchall.return_value = []
    db.cursor.return_value = cursor
    db.__enter__ = Mock(return_value=db)
    db.__exit__ = Mock(return_value=None)
    
    def override_get_db():
        yield db
    
    App.dependency_overrides[get_db] = override_get_db
    client = TestClient(App)
    
    yield client
    
    App.dependency_overrides.clear()


@pytest.fixture
def client_with_db_error():
    """Create a TestClient where the database raises an OperationalError."""
    def override_get_db():
        db = MagicMock(spec=sqlite3.Connection)
        cursor = MagicMock()
        cursor.execute.side_effect = sqlite3.OperationalError("Database is locked")
        db.cursor.return_value = cursor
        db.__enter__ = Mock(return_value=db)
        db.__exit__ = Mock(return_value=None)
        yield db
    
    App.dependency_overrides[get_db] = override_get_db
    client = TestClient(App)
    
    yield client
    
    App.dependency_overrides.clear()
