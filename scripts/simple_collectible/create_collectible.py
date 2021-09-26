from brownie import SimpleCollectible, accounts, network, config
from scripts.helpful_scripts import OPENSEA_FORMAT

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"


def main():
    dev = accounts.add(config["wallets"]["from_key"]) # Add account
    print(network.show_active()) # print current network
    simple_collectible = SimpleCollectible[len(SimpleCollectible) - 1] # get latest simple collectible contract
    token_id = simple_collectible.tokenCounter() # Get amount of tokens created
    transaction = simple_collectible.createCollectible(sample_token_uri, {"from": dev}) # Create token with image uploaded to ipfs
    transaction.wait(1)
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(simple_collectible.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')