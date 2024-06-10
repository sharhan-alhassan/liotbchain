# db.py
import psycopg2
from psycopg2.extras import RealDictCursor
from ..block import Block
import json
from ..utils import DatabaseConnectionError, DatabaseConfigurationError
from liotbchain.utils import logger


def create_database(db_url):
    """
    Creates the PostgreSQL database table for storing blockchain blocks if it doesn't already exist.
    
    The table schema includes:
        - "index" (SERIAL PRIMARY KEY): The unique identifier for each block.
        - "data" (TEXT): The JSON-encoded data of the block.
        - "timestamp" (DOUBLE PRECISION): The timestamp of when the block was created.
        - "previous_hash" (TEXT): The hash of the previous block in the chain.
        - "nonce" (INTEGER): The nonce value used for the proof-of-work algorithm.
        - "hash" (TEXT): The hash of the current block.

    Args:
        db_url (str): The URL for the PostgreSQL database.
    
    Raises:
        DatabaseConfigurationError: If the database URL is missing.
        DatabaseConnectionError: If there is an error connecting to the database.
    """
    if not db_url:
        raise DatabaseConfigurationError("Database URL is missing. Please provide a valid DATABASE_URL.")
    try:
        conn = psycopg2.connect(db_url)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS blocks (
            "index" SERIAL PRIMARY KEY,
            "data" TEXT,
            "timestamp" DOUBLE PRECISION,
            "previous_hash" TEXT,
            "nonce" INTEGER,
            "hash" TEXT
        )''')
        conn.commit()
        conn.close()
    except psycopg2.Error as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise DatabaseConnectionError(f"Failed to connect to the database: {e}")


def save_block(block, db_url):
    """
    Saves a block to the PostgreSQL database.
    
    Args:
        block (Block): The block to be saved, containing index, data, timestamp, previous_hash, nonce, and hash attributes.
        db_url (str): The URL for the PostgreSQL database.
    
    Raises:
        DatabaseConfigurationError: If the database URL is missing.
        DatabaseConnectionError: If there is an error saving the block to the database.
    """
    if not db_url:
        raise DatabaseConfigurationError("Database URL is missing. Please provide a valid DATABASE_URL.")
    try:
        conn = psycopg2.connect(db_url)
        c = conn.cursor()
        c.execute('''INSERT INTO blocks ("index", "data", "timestamp", "previous_hash", "nonce", "hash") VALUES (%s, %s, %s, %s, %s, %s)''', (
            block.index,
            json.dumps(block.data),
            block.timestamp,
            block.previous_hash,
            block.nonce,
            block.hash
        ))
        conn.commit()
        conn.close()
        logger.info(f"Block saved with index: {block.index}")
    except psycopg2.Error as e:
        logger.error(f"Error saving block with index {block.index}: {e}")
        raise DatabaseConnectionError(f"Error saving block with index {block.index}: {e}")

def load_blocks(db_url):
    """
    Loads all blocks from the PostgreSQL database in ascending order of their index.
    
    Args:
        db_url (str): The URL for the PostgreSQL database.
    
    Returns:
        list: A list of Block objects loaded from the database.
    
    Raises:
        DatabaseConfigurationError: If the database URL is missing.
        DatabaseConnectionError: If there is an error loading the blocks from the database.
    """
    if not db_url:
        raise DatabaseConfigurationError("Database URL is missing. Please provide a valid DATABASE_URL.")
    try:
        conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
        c = conn.cursor()
        c.execute('SELECT * FROM blocks ORDER BY "index" ASC')
        blocks = []
        for row in c.fetchall():
            block = Block(
                index=row['index'],
                timestamp=row['timestamp'],
                data=json.loads(row['data']),
                previous_hash=row['previous_hash'],
                nonce=row['nonce'],
                hash=row['hash'],
            )
            blocks.append(block)
        conn.close()
        return blocks
    except psycopg2.Error as e:
        logger.error(f"Error loading blocks: {e}")
        raise DatabaseConnectionError(f"Error loading blocks: {e}")
