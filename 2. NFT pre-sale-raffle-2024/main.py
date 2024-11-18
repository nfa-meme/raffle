from web3 import Web3
import csv
import random

MIN_AMOUNT = 0.03  # Minimum amount in ETH

# Current block as of the code was written: 21,212,423
# Aiming for block 21,214,373 which is around 12 noon UTC on 11/18/2024
DECISION_BLOCK_NUMBER = 21214373

# Connect to Ethereum node (replace with your node URL)
w3 = Web3(Web3.HTTPProvider('https://ethereum-rpc.publicnode.com'))

def get_eligible_addresses(csv_file: str) -> list:
    eligible_addresses = []

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) > 0:
                amount = float(row[1])
                if amount >= MIN_AMOUNT:
                    # Calculate the number of times to add the address based on the amount
                    count = int(amount / MIN_AMOUNT)  # Determine how many times to add the address
                    eligible_addresses.extend([row[0]] * count)  # Add the address 'count' times

    return eligible_addresses

def get_random_addresses(addresses: list, block_number: int, size: int) -> str:
    # Seed with a combination of block_number and size
    random.seed(block_number + size)

    # Select a random address deterministically
    selected_address = random.choice(addresses)

    return selected_address

def main():
    print("Getting eligible addresses...")
    csv_file = 'address.csv'
    eligible_addresses = get_eligible_addresses(csv_file)

    print("Getting random addresses...")
    block = w3.eth.get_block(DECISION_BLOCK_NUMBER)

    # Let's use size for the seed
    seed = block['size']

    random_address = get_random_addresses(eligible_addresses, DECISION_BLOCK_NUMBER, seed)

    print(f'The winner is {random_address}')

if __name__ == "__main__":
    main()
