from scripts.helpful_scripts import get_account, get_contract, fund_with_link, OPENSEA_FORMAT
from brownie import config, network, interface, AdvancedCollectible



def deploy_and_create():
    account = get_account() # Get account
    advanced_collectible = AdvancedCollectible.deploy( # Deploy contract with contract params
        get_contract('vrf_coordinator'),
        get_contract('link_token'),
        config['networks'][network.show_active()]['keyhash'],
        config['networks'][network.show_active()]['fee'],
        {'from':account})
    fund_with_link(advanced_collectible) # fund contract with link
    creating_tx = advanced_collectible.createCollectible({'from':account}) # Create collectible
    creating_tx.wait(1)
    print('New token has been created!')
    return advanced_collectible, creating_tx

def main():
    deploy_and_create()