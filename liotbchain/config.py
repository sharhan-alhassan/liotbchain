import os
from dotenv import load_dotenv, find_dotenv

# Load .env file
load_dotenv(find_dotenv(), override=True)

# Default configuration
DEFAULT_DATABASE_URL = "default_db_url"
DEFAULT_TRANSACTIONS_PER_BLOCK = 2
DEFAULT_DIFFICULTY = 2
DEFAULT_NONCE_LIMIT = 1000000

# Database URL for PostgreSQL database connection
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

# Number of transactions to be grouped into a single block
# Default is 1 transaction per block
TRANSACTIONS_PER_BLOCK = int(os.getenv("TRANSACTIONS_PER_BLOCK", DEFAULT_TRANSACTIONS_PER_BLOCK))

# Mining difficulty: the number of leading zeros required in the block hash
# Default is 4
# Warning: Setting a high value increases the time and computational resources needed for mining
DIFFICULTY = int(os.getenv("DIFFICULTY", DEFAULT_DIFFICULTY))

# Nonce limit to prevent infinite loops during the mining process
# Default is 1000000
# Warning: Setting a very high value can lead to long mining times and excessive computational resource usage
NONCE_LIMIT = int(os.getenv("NONCE_LIMIT", DEFAULT_NONCE_LIMIT))
