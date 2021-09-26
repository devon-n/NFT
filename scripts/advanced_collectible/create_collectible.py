from scripts.helpful_scripts import get_account, fund_with_link
from brownie import network, AdvancedCollectible
from web3 import Web3



def create_collectible(): # Function to create a collectible 
    account = get_account() # Get first account
    advanced_collectible = AdvancedCollectible[-1] # Get latest deployment
    fund_with_link(advanced_collectible.address, amount=Web3.toWei(0.1, 'ether')) # Fund the contract with 0.1 ether in link
    creation_transaction = advanced_collectible.createCollectible({'from': account}) # Call createCollectible function from smart contract
    creation_transaction.wait(1)
    print('Collectible created!')

def main():
    create_collectible()