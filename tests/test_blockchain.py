import pytest
from liotbchain.blockchain import Blockchain
from liotbchain.utils import MiningFailedError, InvalidBlockError, InvalidChainError
import time

@pytest.fixture
def blockchain(mock_db):
    return Blockchain(db_url="postgresql://user:password@localhost:5432/testdb", difficulty=2, nonce_limit=1000, transactions_per_block=2)

def test_create_genesis_block(blockchain):
    assert len(blockchain.chain) == 1
    assert blockchain.chain[0].index == 0
    assert blockchain.chain[0].previous_hash == "0"

def test_add_transaction(blockchain):
    transaction = {"device": "Raspberry Pi", "distance": 100, "timestamp": time.time()}
    blockchain.add_transaction(transaction)
    
    assert len(blockchain.transactions) == 1

def test_mine_block(blockchain, mock_db):
    transaction = {"device": "Raspberry Pi", "distance": 100, "timestamp": time.time()}
    blockchain.add_transaction(transaction)
    blockchain.add_transaction(transaction)
    
    # Setup the return value for fetching the max index
    mock_db.fetchone.return_value = [0]

    new_block = blockchain.mine_block()
    
    assert new_block.index == 1
    assert len(blockchain.chain) == 2
    assert len(blockchain.transactions) == 0

def test_is_chain_valid(blockchain, mock_db):
    transaction = {"device": "Raspberry Pi", "distance": 100, "timestamp": time.time()}
    blockchain.add_transaction(transaction)
    blockchain.add_transaction(transaction)
    
    # Setup the return value for fetching the max index
    mock_db.fetchone.return_value = [0]

    blockchain.mine_block()
    
    assert blockchain.is_chain_valid() == True

    # Tamper with the blockchain
    blockchain.chain[1].data = [{"device": "Tampered Device", "distance": 100, "timestamp": time.time()}]

    with pytest.raises(InvalidBlockError):
        blockchain.is_chain_valid()
