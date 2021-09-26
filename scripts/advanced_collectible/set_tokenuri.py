from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import get_breed, get_account, OPENSEA_FORMAT

metadata_dict = {
    'BROWN': 'https://ipfs.io/ipfs/QmPbVF2MEqMXZMjfa5XrWv4Ji8ggq4nMCJYUgusVAmnY5H?filename=brown.png',
    'BLACK': 'https://ipfs.io/ipfs/dj3udnabJAO3Jjl3Jisdnlaopasdj432nMLSJ2dlfaaeiq?filename=black.png',
    'WHITE': 'https://ipfs.io/ipfs/bVF2MEqMXZMjkjh234h234khoi23q88JSDFisoowyqdmvz?filename=white.png'
}

def main():
    advanced_collectible = AdvancedCollectible[-1] # Get last deployed AdvancedCollectible contract
    number_of_collectibles = advanced_collectible.tokenCounter() # Get amount of tokens created
    for token_id in range(number_of_collectibles): # For each token
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id)) # Get breed
        if not advanced_collectible.tokenURI(token_id).startswith('https://'): # If token has a uri
            print(f'Setting tokenURI of {token_id}')
            set_tokenURI(token_id, advanced_collectible, metadata_dict[breed]) # Set token uri


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {'from':account})
    tx.wait(1)
    print(f'Set token URI at {OPENSEA_FORMAT.format(nft_contract.address, token_id}')