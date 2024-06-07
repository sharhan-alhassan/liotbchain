import pytest
from liotbchain.database.db import create_database, save_block, load_blocks
from liotbchain.block import Block
import time
import json

@pytest.fixture
def setup_mock_db(mock_db):
    # Setup: Ensure the table exists
    mock_db.execute.assert_called_with('''CREATE TABLE IF NOT EXISTS blocks (
        "index" SERIAL PRIMARY KEY,
        "data" TEXT,
        "timestamp" DOUBLE PRECISION,
        "previous_hash" TEXT,
        "nonce" INTEGER,
        "hash" TEXT
    )''')

def test_create_database(mock_db):
    create_database(db_url="postgresql://user:password@localhost:5432/testdb")
    # Check if the table creation SQL was executed
    mock_db.execute.assert_called_with('''CREATE TABLE IF NOT EXISTS blocks (
        "index" SERIAL PRIMARY KEY,
        "data" TEXT,
        "timestamp" DOUBLE PRECISION,
        "previous_hash" TEXT,
        "nonce" INTEGER,
        "hash" TEXT
    )''')

def test_save_and_load_block(mock_db, setup_mock_db):
    index = 0
    timestamp = time.time()
    data = [{"device": "Raspberry Pi", "distance": 100, "timestamp": timestamp}]
    previous_hash = "0"
    block = Block(index, timestamp, data, previous_hash)
    block.hash = block.calculate_hash()

    save_block(block, db_url="postgresql://user:password@localhost:5432/testdb")

    # Check if the block was inserted into the mock DB
    mock_db.execute.assert_any_call('''INSERT INTO blocks ("index", "data", "timestamp", "previous_hash", "nonce", "hash") VALUES (%s, %s, %s, %s, %s, %s)''',
                                    (block.index, json.dumps(data), block.timestamp, block.previous_hash, block.nonce, block.hash))

    # Setup the return value for loading blocks
    mock_db.fetchall.return_value = [{
        'index': block.index,
        'data': json.dumps(data),
        'timestamp': block.timestamp,
        'previous_hash': block.previous_hash,
        'nonce': block.nonce,
        'hash': block.hash
    }]

    blocks = load_blocks(db_url="postgresql://user:password@localhost:5432/testdb")

    assert len(blocks) == 1
    assert blocks[0].index == block.index
    assert blocks[0].timestamp == block.timestamp
    assert blocks[0].data == data
    assert blocks[0].previous_hash == block.previous_hash
    assert blocks[0].nonce == block.nonce
    assert blocks[0].hash == block.hash
