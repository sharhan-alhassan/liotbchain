from liotbchain import Blockchain
import time

def main():
    # Initialize the blockchain
    blockchain = Blockchain()

    # Add transactions
    transaction1 = {"device": "Raspberry Pi 1", "distance": 120, "timestamp": time.time()}
    transaction2 = {"device": "Raspberry Pi 2", "distance": 150, "timestamp": time.time()}
    transaction3 = {"device": "Raspberry Pi 3", "distance": 130, "timestamp": time.time()}

    blockchain.add_transaction(transaction1)
    blockchain.add_transaction(transaction2)
    blockchain.add_transaction(transaction3)

    # Mine a block
    blockchain.mine_block()

    # Display the blockchain
    for block in blockchain.get_chain():
        print(f"Block {block.index}: Transactions={block.data}, Nonce={block.nonce}, Hash={block.hash}, Merkle Root={block.merkle_root}")

    # Validate the blockchain
    if blockchain.is_chain_valid():
        print("The blockchain is valid.")
    else:
        print("The blockchain is not valid.")

if __name__ == "__main__":
    main()
