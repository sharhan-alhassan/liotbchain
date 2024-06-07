import pytest
import psycopg2
from liotbchain.database.db import create_database, save_block, load_blocks
from liotbchain.block import Block
import time
import json

DATABASE_URL = "your_postgres_db_url"

@pytest.fixture
def setup_database():
    create_database(DATABASE_URL)
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('DELETE FROM blocks')
    conn.commit()
    conn.close()

def test_create_database(setup_database):
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute("SELECT to_regclass('public.blocks')")
    result = c.fetchone()[0]
    conn.close()
    
    assert result == 'blocks'

def test_save_and_load_block(setup_database):
    index = 0
    timestamp = time.time()
    data = [{"device": "Raspberry Pi", "distance": 100, "timestamp": timestamp}]
    previous_hash = "0"
    block = Block(index, timestamp, data, previous_hash)
    block.hash = block.calculate_hash()

    save_block(block, DATABASE_URL)
    
    blocks = load_blocks(DATABASE_URL)
    
    assert len(blocks) == 1
    assert blocks[0].index == block.index
    assert blocks[0].timestamp == block.timestamp
    assert blocks[0].data == block.data
    assert blocks[0].previous_hash == block.previous_hash
    assert blocks[0].nonce == block.nonce
    assert blocks[0].hash == block.hash
