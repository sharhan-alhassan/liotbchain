import hashlib
import json
from .utils import BlockchainOperationError
from collections import OrderedDict
from liotbchain.utils import logger

class Block:
    """
    Represents a block in the blockchain.

    Attributes:
        index (int): The block's index within the blockchain.
        timestamp (float): The timestamp of when the block was created.
        data (list): The transactions stored within the block.
        previous_hash (str): The hash of the block's predecessor.
        nonce (int): The nonce used for the proof-of-work.
        hash (str): The hash of the current block.
    """

    def __init__(self, index, timestamp, data, previous_hash, nonce=0, hash=None, merkle_root=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash
        self.merkle_root = merkle_root


    def calculate_hash(self):
        """
        Calculates the SHA-256 hash of the block.

        Returns:
            str: The hexadecimal string of the hash.
        """
        try:
            # Creating an ordered dictionary to keep the block information consistent for hashing
            block_dict = OrderedDict({
                'index': self.index,
                'timestamp': self.timestamp,
                'data': self.data,
                'previous_hash': self.previous_hash,
                'nonce': self.nonce,
                'merkle_root': self.calculate_merkle_root()
            })
            block_string = json.dumps(block_dict, sort_keys=True).encode()
            return hashlib.sha256(block_string).hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate hash: {str(e)}")
            raise BlockchainOperationError(f"Failed to calculate hash: {str(e)}")

    def calculate_merkle_root(self):
        """
        Calculates the Merkle root hash of the block's transactions.

        Returns:
            str: The hexadecimal string of the Merkle root hash.
        """
        try:
            transactions = [json.dumps(tx, sort_keys=True).encode() for tx in self.data]
            if len(transactions) == 0:
                return ''
            elif len(transactions) == 1:
                return hashlib.sha256(transactions[0]).hexdigest()
            else:
                return self._calculate_merkle_root(transactions)
        except Exception as e:
            logger.error(f"Failed to calculate Merkle root: {str(e)}")
            raise BlockchainOperationError(f"Failed to calculate Merkle root: {str(e)}")

    def _calculate_merkle_root(self, transactions):
        """
        Helper method to recursively calculate the Merkle root hash.

        Args:
            transactions (list): List of transaction hashes.

        Returns:
            str: The hexadecimal string of the Merkle root hash.
        """
        if len(transactions) == 1:
            return hashlib.sha256(transactions[0]).hexdigest()

        new_level = []

        for i in range(0, len(transactions), 2):
            left = transactions[i]
            right = transactions[i + 1] if i + 1 < len(transactions) else left
            new_hash = hashlib.sha256(left + right).hexdigest().encode()
            new_level.append(new_hash)

        return self._calculate_merkle_root(new_level)
