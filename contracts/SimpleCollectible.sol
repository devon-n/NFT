// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

// Imports
import '@openzeppelin/contracts/token/ERC721/ERC721.sol'; 

contract SimpleCollectible is ERC721 { // Inherit from contract

    uint256 public tokenCounter; // init var to keep track of number of tokens

    constructor () public ERC721('Dogie', 'DOG'){ // Constructor function to set name and ticker symbol

    }

    function createCollectible(string memory tokenURI) public returns (uint256) { // Function to create a token
        uint256 newTokenId = tokenCounter; // Set token id to counter
        _safeMint(msg.sender, newTokenId); // Call inherited function to mint token 
        _setTokenURI(newTokenId, tokenURI); // Call inherited function to set token URI
        tokenCounter++; // increment token count 
        return newTokenId; // return token id
    }    
}