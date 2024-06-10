

from liotbchain.blockchain import Blockchain
from liotbchain.utils import InvalidChainError
import time

def main():
    try:
        # Create a new Blockchain instance with a specified difficulty level
        my_blockchain = Blockchain()  # You can adjust the difficulty for testing

        # Data from IoT devices
        iot_data = [
            {"device": "Raspberry Pi 1", "distance": 120, "timestamp": time.time()},
            {"device": "Raspberry Pi 2", "distance": 151, "timestamp": time.time()},
            {"device": "Raspberry Pi 3", "distance": 130, "timestamp": time.time()},
            {"device": "Raspberry Pi 4", "distance": 140, "timestamp": time.time()},
        ]

        # Simulate the process of receiving data and adding transactions
        for data in iot_data:
            my_blockchain.add_transaction(data)
            print(f"Transaction added for device {data['device']}.")

        # # Display the blockchain
        # print("\nFull Blockchain:")
        # for block in my_blockchain.get_chain():
        #     print(f"Block {block.index}: Transactions={block.data}, Nonce={block.nonce}, Hash={block.hash}, Merkle Root={block.calculate_merkle_root()}")

        # Display the blockchain
        print("\nFull Blockchain:")
        for block in my_blockchain.get_chain():
            # print(f"Full block: {block}")
            print(f"Block {block.index}: Transactions={block.data}, Timestamp-{block.timestamp}, Nonce={block.nonce}, Previous Hash={block.previous_hash}, Hash={block.hash}")


        # Validate the integrity of the blockchain
        if my_blockchain.is_chain_valid():
            print("\nThe blockchain is valid.")
        else:
            print("\nThe blockchain is not valid.")
    except InvalidChainError as e:
        print(f"Blockchain validation failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
