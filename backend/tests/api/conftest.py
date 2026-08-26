import pytest
from unittest.mock import MagicMock, AsyncMock, patch

@pytest.fixture(autouse=True)
def mock_db_singleton():
    from app.config.database import db
    
    # Mock the internal database object
    mock_database = MagicMock()
    mock_database.users = MagicMock()
    mock_database.users.find_one = AsyncMock(return_value=None)
    mock_database.users.insert_one = AsyncMock()
    
    # Set the singleton's database property
    db.database = mock_database
    
    with patch.object(db, "connect_db", new_callable=AsyncMock), \
         patch.object(db, "close_db", new_callable=AsyncMock):
        yield mock_database
