from .block import Block
from .utils import InvalidBlockError, InvalidChainError, MiningFailedError, DatabaseConfigurationError
from .database.db import create_database, save_block, load_blocks
import time
import psycopg2
from liotbchain.config import DATABASE_URL, TRANSACTIONS_PER_BLOCK, DIFFICULTY, NONCE_LIMIT
from liotbchain.utils import logger


class Blockchain:
    """
    Blockchain implementation with proof-of-work mechanism.

    Attributes:
        chain (list): A list of blocks that form the blockchain.
        difficulty (int): The number of leading zeros required in the hash.
        transactions (list): A list to hold transactions temporarily until a block is created.
        transactions_per_block (int): The number of transactions to be grouped into a single block.
        nonce_limit (int): The maximum limit for nonce to prevent infinite loops.
    """
    def __init__(self, difficulty=None, nonce_limit=None, db_url=None, transactions_per_block=None):
        self.chain = []
        self.difficulty = difficulty or DIFFICULTY  # Difficulty for the proof of work algorithm
        self.nonce_limit = nonce_limit or NONCE_LIMIT  # Limit to prevent infinite loops
        self.transactions = []  # Temporary storage for transactions
        self.db_url = db_url or DATABASE_URL
        if not self.db_url:
            raise DatabaseConfigurationError("Database URL is missing. Please provide a valid DATABASE_URL.")
        self.transactions_per_block = transactions_per_block or TRANSACTIONS_PER_BLOCK
        self.initialize_blockchain()


    def create_genesis_block(self):
        """
        Generates the genesis block and appends it to the blockchain.

        Returns:
            Block: The genesis block with predefined values.
        """
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        genesis_block.hash = genesis_block.calculate_hash()  # Set the hash for the genesis block
        self.chain.append(genesis_block)
        save_block(genesis_block, self.db_url)  # Save the genesis block to the database
        logger.info(f"Genesis block created with index: {genesis_block.index}")


    def initialize_blockchain(self):
        """
        Initializes the blockchain by creating the database and loading existing blocks from the database.
        If no existing blocks are found, it creates the genesis block.
        """
        create_database(self.db_url)
        loaded_blocks = load_blocks(self.db_url)
        if loaded_blocks:
            self.chain = loaded_blocks
        else:
            self.create_genesis_block()
        logger.info(f"Blockchain initialized with {len(self.chain)} blocks.")


    def save_blockchain(self):
        """
        Saves the entire blockchain to the database.
        """
        for block in self.chain:
            save_block(block, self.db_url)


    def add_block(self, block):
        """
        Adds a new block to the blockchain after performing proof-of-work.

        Args:
            block (Block): The block to be added to the blockchain.

        Raises:
            InvalidBlockError: If the block cannot be added to the blockchain.
        """
        try:
            block.previous_hash = self.get_latest_block().hash
            # block.merkle_root = block.calculate_merkle_root()  # Calculate the Merkle root before hashing
            block.hash = self.proof_of_work(block)  # Calculate the hash after setting previous_hash and merkle_root
            self.chain.append(block)
            save_block(block, self.db_url)  # Save the updated blockchain to the database
            logger.info(f"Block added with index: {block.index}")
        except Exception as e:
            logger.error(f"Error in add_block: {str(e)}")
            raise InvalidBlockError(f"Failed to add block: {str(e)}")


    def proof_of_work(self, block):
        """
        Performs the proof of work to adjust the block's nonce until the hash meets the blockchain difficulty.

        Args:
            block (Block): The block for which the nonce is adjusted.

        Returns:
            str: The hash of the block that satisfies the difficulty criteria.

        Raises:
            MiningFailedError: If the mining process fails to find a valid hash within the threshold.
        """
        block.nonce = 0
        block.hash = block.calculate_hash()
        block.merkle_root = block.calculate_merkle_root()
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()
            if block.nonce > self.nonce_limit:  # Use the configurable limit to prevent infinite loops
                raise MiningFailedError("Mining failed: Nonce exceeds threshold")
        return block.hash

    def is_chain_valid(self):
        """
        Validates the blockchain's integrity by ensuring each block's link and proof-of-work are correct.

        Returns:
            bool: True if the blockchain is valid, otherwise raises InvalidChainError.
        """
        try:
            for i in range(1, len(self.chain)):
                current = self.chain[i]
                previous = self.chain[i - 1]

                if current.hash != current.calculate_hash():
                    logger.error(f"Hash mismatch: Block {i}'s stored hash {current.hash} does not match calculated hash {current.calculate_hash()}.")
                    raise InvalidBlockError(f"Hash mismatch: Block {i}'s stored hash {current.hash} does not match calculated hash {current.calculate_hash()}.")
                if current.previous_hash != previous.hash:
                    logger.error(f"Link error: Block {i}'s previous hash {current.previous_hash} does not link to Block {i-1}'s hash {previous.hash}.")
                    raise InvalidBlockError(f"Link error: Block {i}'s previous hash {current.previous_hash} does not link to Block {i-1}'s hash.")
                if not current.hash.startswith('0' * self.difficulty):
                    logger.error(f"Proof of Work error: Block {i}'s hash {current.hash} does not meet the difficulty requirement.")
                    raise InvalidBlockError(f"Proof of Work error: Block {i}'s hash {current.hash} does not meet the difficulty requirement.")

            return True
        except InvalidChainError as e:
            return False

    def get_latest_block(self):
        """
        Retrieves the most recent block in the blockchain.

        Returns:
            Block: The latest block in the chain.
        """
        return self.chain[-1]

    def add_transaction(self, transaction):
        """
        Adds a transaction to the temporary storage. When the number of transactions reaches
        the configured TRANSACTIONS_PER_BLOCK, a new block is mined and added to the blockchain.

        Args:
            transaction: The transaction data to be added.
        """
        self.transactions.append(transaction)
        if len(self.transactions) >= self.transactions_per_block:
            self.mine_block()

    def mine_block(self):
        """
        Mines a new block with the current transactions. Resets the transactions list after mining.

        Returns:
            Block: The newly mined block, now part of the blockchain.

        Raises:
            MiningFailedError: If the mining process fails.
        """
        try:
            # Get the maximum index from the database
            with psycopg2.connect(self.db_url) as conn:
                c = conn.cursor()
                c.execute('SELECT MAX("index") FROM blocks')
                max_index = c.fetchone()[0]
                if max_index is None:
                    max_index = 0
                logger.info(f"Max index from database: {max_index}")

            new_index = max_index + 1  # Ensure the new block receives a unique index
            logger.info(f"New block index: {new_index}")
            new_block = Block(new_index, time.time(), self.transactions, self.get_latest_block().hash if self.chain else "0")
            self.add_block(new_block)  # Add the newly mined block to the chain
            self.transactions = []  # Reset transactions
            return new_block

        except Exception as e:
            logger.error(f"Error in mine_block: {str(e)}")
            raise MiningFailedError(f"Failed to mine block: {str(e)}")

    def get_chain(self):
        """
        Retrieves the entire blockchain from the database.

        Returns:
            list: The list of blocks that comprise the blockchain.
        """
        return load_blocks(self.db_url)
