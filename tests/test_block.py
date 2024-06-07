import pytest
from liotbchain.block import Block
import time
import json

@pytest.fixture
def block():
    index = 0
    timestamp = time.time()
    data = [{"device": "Raspberry Pi", "distance": 100, "timestamp": timestamp}]
    previous_hash = "0"
    block = Block(index, timestamp, data, previous_hash)
    return block

def test_block_initialization(block):
    assert block.index == 0
    assert block.previous_hash == "0"
    assert block.nonce == 0
    assert block.hash is None
    assert block.data == [{"device": "Raspberry Pi", "distance": 100, "timestamp": block.timestamp}]

def test_calculate_hash(block):
    calculated_hash = block.calculate_hash()
    assert calculated_hash is not None
    assert isinstance(calculated_hash, str)

def test_calculate_merkle_root(block):
    merkle_root = block.calculate_merkle_root()
    assert merkle_root is not None
    assert isinstance(merkle_root, str)
