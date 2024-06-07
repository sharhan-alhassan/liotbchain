
import os
import pytest
from dotenv import load_dotenv
from unittest.mock import MagicMock, patch
import sys
# Load environment variables from .env file
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope='session', autouse=True)
def load_env():
    os.environ['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/testdb')
    os.environ['TRANSACTIONS_PER_BLOCK'] = os.getenv('TRANSACTIONS_PER_BLOCK', '1')
    os.environ['DIFFICULTY'] = os.getenv('DIFFICULTY', '3')
    os.environ['NONCE_LIMIT'] = os.getenv('NONCE_LIMIT', '1000000')

@pytest.fixture
def mock_db():
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_cursor

