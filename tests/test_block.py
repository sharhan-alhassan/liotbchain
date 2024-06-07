import pytest
from liotbchain.block import Block
import time

def test_block_initialization():
    index = 0
    timestamp = time.time()
    data = [{"device": "Raspberry Pi", "distance": 100, "timestamp": timestamp}]
    previous_hash = "0"
    block = Block(index, timestamp, data, previous_hash)
    
    assert block.index == index
    assert block.timestamp == timestamp
    assert block.data == data
    assert block.previous_hash == previous_hash
    assert block.nonce == 0
    assert block.hash is None

def test_calculate_hash():
    index = 0
    timestamp = time.time()
    data = [{"device": "Raspberry Pi", "distance": 100, "timestamp": timestamp}]
    previous_hash = "0"
    block = Block(index, timestamp, data, previous_hash)
    block.hash = block.calculate_hash()

    assert block.hash is not None
    assert len(block.hash) == 64

def test_calculate_merkle_root():
    index = 0
    timestamp = time.time()
    data = [{"device": "Raspberry Pi", "distance": 100, "timestamp": timestamp}]
    previous_hash = "0"
    block = Block(index, timestamp, data, previous_hash)
    merkle_root = block.calculate_merkle_root()

    assert merkle_root is not None
    assert len(merkle_root) == 64
