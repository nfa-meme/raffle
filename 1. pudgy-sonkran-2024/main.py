import logging
from typing import List, Tuple

from os import getenv
from web3 import Web3


def get_list_of_purchases(file_path: str) -> tuple[List[str], List[str]]:
    """
    Read the CSV file and return the list of purchases for raffle
    """
    list_of_purchases = []
    list_of_pudgy_event_purchases = []

    with open(file_path, "r") as file:
        for line in file:
            row = line.split(",")
            order_id = row[0]
            discount_code = row[12]

            list_of_purchases.append(order_id)
            if discount_code.upper() == "BKKDAMNHOT":
                list_of_pudgy_event_purchases.append(order_id)

    return list_of_purchases, list_of_pudgy_event_purchases


def get_main_event_winner(
    withdrawals: List, list_of_purchase: List
) -> Tuple[List[str], List[str]]:
    """
    This method will return the winners for the main event
    which are USDC and Lil Pudgy winners.
    """
    usdc_winners = list()
    lil_pudgy_winners = list()

    # We will draw USDC winners first
    for withdrawal in withdrawals:
        if len(usdc_winners) == 5:
            break
        withdrawal_amount = int(withdrawal["amount"])
        position = withdrawal_amount % len(list_of_purchase)

        if list_of_purchase[position] not in usdc_winners:
            usdc_winners.append(list_of_purchase[position])

    # And then Lil Pudgy winner
    for withdrawal in withdrawals:
        withdrawal_amount = int(withdrawal["amount"])
        position = withdrawal_amount % len(list_of_purchase)

        if (
            list_of_purchase[position] not in usdc_winners
            and list_of_purchase[position] not in lil_pudgy_winners
        ):
            lil_pudgy_winners.append(list_of_purchase[position])
            break

    return usdc_winners, lil_pudgy_winners


def get_pudgy_event_winners(
    withdrawals: List, list_of_purchase: List
) -> Tuple[List[str], List[str]]:
    """
    This method will return the winners for the Pudgy Songkran Event
    that has used the discount code "BKKDAMNHOT" which was shared
    during the Pudgy Songkran event in Bangkok.

    The winners in Pudgy Event can still stand a chance at winning
    the main event.
    """
    usdc_winners = list()
    gk_winners = list()

    # We will draw USDC winners first
    for withdrawal in withdrawals[-10:]:
        if len(usdc_winners) == 5:
            break
        withdrawal_amount = int(withdrawal["amount"])
        position = withdrawal_amount % len(list_of_purchase)

        if list_of_purchase[position] not in usdc_winners:
            usdc_winners.append(list_of_purchase[position])

    # And then GK winners
    for withdrawal in withdrawals[int(len(withdrawals) / 2) :]:
        if len(gk_winners) == 2:
            break

        withdrawal_amount = int(withdrawal["amount"])
        position = withdrawal_amount % len(list_of_purchase)

        if (
            list_of_purchase[position] not in usdc_winners
            and list_of_purchase[position] not in gk_winners
        ):
            gk_winners.append(list_of_purchase[position])

    return usdc_winners, gk_winners


def main():
    # Make sure Project ID is set
    INFURA_PROJECT_ID = getenv("INFURA_PROJECT_ID", None)
    if INFURA_PROJECT_ID is None:
        raise ValueError("Please set the INFURA_PROJECT_ID environment variable")

    # BLOCK_NUMBER = getenv("BLOCK_NUMBER", None)
    # if BLOCK_NUMBER is None:
    #     raise ValueError("Please set the BLOCK_NUMBER environment variable")

    CSV_FILE = getenv("CSV_FILE", None)
    if CSV_FILE is None:
        raise ValueError("Please set the CSV_FILE environment variable")

    # Connect to an Ethereum node (e.g., Infura)
    w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}"))

    # Get Block Info
    latest_block = w3.eth.block_number
    block_info = w3.eth.get_block(latest_block)
    withdrawals = block_info["withdrawals"]

    list_of_purchases, list_of_pudgy_event_purchases = get_list_of_purchases(CSV_FILE)

    # Get index for the all winners
    usdc_lucky_winner_index, lil_pudgy_winner_index = get_main_event_winner(
        withdrawals, list_of_purchases
    )
    usdc_pudgy_songkran_winner_index, gk_pudgy_songkran_winner_index = (
        get_pudgy_event_winners(withdrawals, list_of_pudgy_event_purchases)
    )

    print("Block Number:", latest_block)
    print("------------------------------------------")
    print("Lil Pudgy Winner is:", lil_pudgy_winner_index)
    print("USDC Winners are:", usdc_lucky_winner_index)
    print("Pudgy Songkran USDC Winners are:", usdc_pudgy_songkran_winner_index)
    print(
        "Pudgy Songkran Galactic Konquest Winners are:", gk_pudgy_songkran_winner_index
    )


if __name__ == "__main__":
    main()
