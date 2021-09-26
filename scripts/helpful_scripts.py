from brownie import accounts, network, config, Contract, LinkToken, VRFCoordinatorMock
from web3 import Web3

# Vars that will be called from other scripts
OPENSEA_FORMAT = 'https://testnets.opensea.io/assets/{}/{}'
NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]

BREED_MAPPING = {0: 'WHITE', 1: 'BLACK', 2:'BROWN'}
contract_to_mock = {'link_token': LinkToken, 'vrf_coordinator': VRFCoordinatorMock}

def get_account(index=None, id=None): # Function to get an account depending on the operating network
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config['wallets']['from_key'])


def get_contract(contract_name): # Function to get a contracts address based on its name
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS: # If local network, deploy a mock
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        try: # Try get address from config file
            contract_address = config["networks"][network.show_active()][contract_name] 
            contract = Contract.from_abi(
                contract_type._name, contract_address, contract_type.abi
            )
        except KeyError:
            print(
                f"{network.show_active()} address not found, perhaps you should add it to the config or deploy mocks?"
            )
            print(
                f"brownie run scripts/deploy_mocks.py --network {network.show_active()}"
            )
    return contract

def fund_with_link(contract_address, account=None, link_token=None, amount=Web3.toWei(1, 'ether')): # Function to fund contracts with link
    account = account if account else get_account() # Get account
    link_token = link_token if link_token else get_contract('link_token') # Get link token address
    funding_tx = link_token.transfer(contract_address, amount, {'from':account}) # transfer link token to contract address
    funding_tx.wait(1)
    print(f'Funded {contract_address}')
    return funding_tx


def deploy_mocks():
    print(f'Active network is {network.show_active()}')
    print('Deploying Mocks')
    account = get_account()
    print('Deploying Mock Link Token')
    link_token = LinkToken.deploy({'from':account})
    print('Deploying Mock VRF Coordinator')
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {'from':account})




def get_breed(breed_number):
    return BREED_MAPPING[breed_number]