import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

# Database URL for PostgreSQL database connection
DATABASE_URL = os.getenv("DATABASE_URL", "default_db_url")

# Number of transactions to be grouped into a single block
# Default is 1 transaction per block
TRANSACTIONS_PER_BLOCK = int(os.getenv("TRANSACTIONS_PER_BLOCK", 1))

# Mining difficulty: the number of leading zeros required in the block hash
# Default is 4
# Warning: Setting a high value increases the time and computational resources needed for mining
DIFFICULTY = int(os.getenv("DIFFICULTY", 4))

# Nonce limit to prevent infinite loops during the mining process
# Default is 1000000
# Warning: Setting a very high value can lead to long mining times and excessive computational resource usage
NONCE_LIMIT = int(os.getenv("NONCE_LIMIT", 1000000))
