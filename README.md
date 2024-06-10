# liotbchain
liotbchain is a lightweight, versatile blockchain framework designed for both IoT and non-IoT applications. It provides a robust and flexible solution for creating, managing, and interacting with blockchains, leveraging Python's simplicity and the efficiency of PostgreSQL for data storage. With configurable parameters for mining difficulty, transaction grouping, and proof-of-work limits, liotbchain adapts to various use cases, ensuring secure and efficient data management across distributed systems.

Disclaimer: liotbchain is not intended for real production environments but aims to leverage the core principles of blockchain technology for running a local, self-created blockchain. It is ideal for educational purposes, prototyping, and small-scale projects


# Installation
To install the liotbchain framework, use the following command:
```sh
pip install liotbchain
```

# Configuration
## Environment Variables
You can configure the liotbchain framework using environment variables:

### Option 1: Set environment variables
```sh
1. Export using the os utility
DATABASE_URL = os.getenv("DATABASE_URL", "default_db_url")

# Number of transactions to be grouped into a single block
# Default is 1 transaction per block
TRANSACTIONS_PER_BLOCK = int(os.getenv("TRANSACTIONS_PER_BLOCK", 1))

# Mining difficulty: the number of leading zeros required in the block hash
# Default is 4
# Warning: Setting a high value increases the time and computational resources needed for mining
DIFFICULTY = int(os.getenv("DIFFICULTY", 3))

# Nonce limit to prevent infinite loops during the mining process
# Default is 1000000
# Warning: Setting a very high value can lead to long mining times and excessive computational resource usage
NONCE_LIMIT = int(os.getenv("NONCE_LIMIT", 1000000))

2. Export variables directly to your working shell/terminal
# Set environment variables before running your script:
# Set the PostgreSQL database URL
export DATABASE_URL="postgresql://username:password@hostname:port/database_name"

# Set the number of transactions per block
export TRANSACTIONS_PER_BLOCK=2

# Set the mining difficulty
export DIFFICULTY=5

# Set the nonce limit to prevent infinite loops during mining
export NONCE_LIMIT=500000

3. Directly set the environment variables in a .env file
DATABASE_URL=
TRANSACTIONS_PER_BLOCK=
DIFFICULTY=
NONCE_LIMIT=

# Then instantiate the Blockchain() without passing any parameters
from liotbchain import Blockchain
blockchain = Blockchain()

```

### Option 2: Instantiate the Blockchain class with parameters:
```sh
from liotbchain import Blockchain

# Instantiate the Blockchain with custom parameters
blockchain = Blockchain(difficulty=5, nonce_limit=500000, db_url="postgresql://username:password@hostname:port/database_name", transactions_per_block=2)

```

# Usage
Adding Transactions and Mining Blocks
You can add transactions to the blockchain and mine blocks:
```py
# Add transactions
transaction1 = {"device": "Raspberry Pi 1", "distance": 120, "timestamp": time.time()}
transaction2 = {"device": "Raspberry Pi 2", "distance": 150, "timestamp": time.time()}
transaction3 = {"device": "Raspberry Pi 3", "distance": 130, "timestamp": time.time()}

blockchain.add_transaction(transaction1)
blockchain.add_transaction(transaction2)
blockchain.add_transaction(transaction3)

# Mine a block when the number of transactions reaches the configured limit
blockchain.mine_block()
```

# Displaying the Blockchain
You can display the entire blockchain:
```py
# Display the blockchain
for block in blockchain.get_chain():
    print(f"Block {block.index}: Transactions={block.data}, Nonce={block.nonce}, Hash={block.hash}, Merkle Root={block.merkle_root}")
```

# Validating the Blockchain
You can validate the integrity of the blockchain:
```py
if blockchain.is_chain_valid():
    print("The blockchain is valid.")
else:
    print("The blockchain is not valid.")
```

# API Reference
Block Class
The Block class represents a block in the blockchain.

## Attributes:
```sh
index (int): The block's index within the blockchain.
timestamp (float): The timestamp of when the block was created.
data (list): The transactions stored within the block.
previous_hash (str): The hash of the block's predecessor.
nonce (int): The nonce used for the proof-of-work.
hash (str): The hash of the block.
merkle_root (str): The Merkle root hash of the block's transactions.
```

## Methods:
```sh
calculate_hash() -> str: Calculates the SHA-256 hash of the block.
calculate_merkle_root() -> str: Calculates the Merkle root hash of the block's transactions.
```

## Blockchain Class
The Blockchain class implements the blockchain with proof-of-work mechanism.

Attributes:
```sh
chain (list): A list of blocks that form the blockchain.
difficulty (int): The number of leading zeros required in the hash.
transactions (list): A list to hold transactions temporarily until a block is created.
nonce_limit (int): The maximum limit for nonce to prevent infinite loops.
```

# Methods:
```sh
__init__(difficulty=None, nonce_limit=None, db_url=None, transactions_per_block=None): Initializes the blockchain with optional configuration parameters.
create_genesis_block(): Generates the genesis block and appends it to the blockchain.
initialize_blockchain(): Initializes the blockchain by creating the database and loading existing blocks from the database.
save_blockchain(): Saves the entire blockchain to the database.
add_block(block): Adds a new block to the blockchain after performing proof-of-work.
proof_of_work(block) -> str: Performs the proof of work to adjust the block's nonce until the hash meets the blockchain difficulty.
is_chain_valid() -> bool: Validates the blockchain's integrity by ensuring each block's link and proof-of-work are correct.
get_latest_block() -> Block: Retrieves the most recent block in the blockchain.
add_transaction(transaction): Adds a transaction to the temporary storage. When the number of transactions reaches the configured limit, a new block is mined and added to the blockchain.
mine_block() -> Block: Mines a new block with the current transactions and adds it to the blockchain.
get_chain() -> list: Retrieves the entire blockchain.
```

- Refer to `docs/example.py` for a sample code
