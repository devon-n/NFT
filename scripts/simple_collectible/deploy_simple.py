import os
from brownie import SimpleCollectible, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"]) # Add account
    print(network.show_active())
    publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False
    SimpleCollectible.deploy({"from": dev}, publish_source=publish_source)