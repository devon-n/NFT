from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

# Mapping of breeds to uri's
breed_to_image_uri = {
    'BROWN': 'https://ipfs.io/ipfs/QmPbVF2MEqMXZMjfa5XrWv4Ji8ggq4nMCJYUgusVAmnY5H?filename=brown.png',
    'BLACK': 'https://ipfs.io/ipfs/dj3udnabJAO3Jjl3Jisdnlaopasdj432nMLSJ2dlfaaeiq?filename=black.png',
    'WHITE': 'https://ipfs.io/ipfs/bVF2MEqMXZMjkjh234h234khoi23q88JSDFisoowyqdmvz?filename=white.png'
}


def main():
    advanced_collectible = AdvancedCollectible[-1] # Get latest contract
    number_of_advanced_collectibles = advanced_collectible.tokenCounter() # get number of tokens created
    print(f'You have created {number_of_advanced_collectibles} collectibles!')

    for token_id in range(number_of_advanced_collectibles): # For each token
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id)) # get the token breed
        metadata_file_name = f'./metadata/{network.show_active()}/{token_id}-{breed}.json' # init metadata file name

        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists(): # if file name already exists print statement
            print(f'{metadata_file_name} already exists. Delete it to overwrite')
        else: # else create metadata file
            print(f'Creating file: {metadata_file_name}')
            collectible_metadata['name'] = breed # Set metadata vars
            collectible_metadata['description'] = f'An adorable {breed}'
            image_path = './img/' + breed.lower().replace('_', '-') + '.png' 

            image_uri = None 
            if os.getenv('UPLOAD_IPFS') == 'true': # If env var == true: upload image to ipfs
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed] # if image_uri exists keep it, else: set it to breed/uri mapping

            collectible_metadata['image'] = image_uri
            with open(metadata_file_name, 'w') as file: # Open file and write json to it
                json.dump(collectible_metadata, file)
            if os.getenv('UPLOAD_IPFS') == 'true':
                upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    with Path(filepath).open('rb') as fp:
        image_binary = fp.read()
        # Upload
        ipfs_url = 'http://127.0.0.1:5001'
        endpoint = '/api/v0/add'
        response = requests.post(ipfs_url + endpoint, files={'file':image_binary})
        ipfs_hash = response.json()['Hash']
        filename = filepath.split('/')[-1:][0]
        image_uri = f'https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}'
        print(image_uri)
        return image_uri