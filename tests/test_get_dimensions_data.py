import pytest
from unittest.mock import patch, MagicMock
import get_dimensions_data

@patch('get_dimensions_data.psycopg2.connect')
@patch.dict('os.environ', {'user': 'user', 'password': 'pw', 'host': 'host', 'port': '5432', 'dbname': 'db'})
def test_connect_and_fetch_dimensions_success(mock_connect):
    """Test successful database connection and data retrieval."""
    # Setup mock cursor and data
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock data returned by fetchall
    expected_data = [{'id': 1, 'dimension': 'Strategy'}]
    mock_cursor.fetchall.return_value = expected_data
    
    # Run function
    result = get_dimensions_data.connect_and_fetch_dimensions()
    
    # Assertions
    mock_connect.assert_called_once()
    mock_cursor.execute.assert_called_with("SELECT * FROM dimensions;")
    assert result == expected_data

@patch('get_dimensions_data.psycopg2.connect')
def test_connect_and_fetch_dimensions_failure(mock_connect):
    """Test handling of connection failure."""
    mock_connect.side_effect = Exception("Connection failed")
    
    result = get_dimensions_data.connect_and_fetch_dimensions()
    
    assert result is None
