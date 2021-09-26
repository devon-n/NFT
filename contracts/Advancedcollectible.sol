// SPDX License-Identifier: MIT License
pragma solidity ^0.6.6;

// Imports
import '@openzeppelin/contracts/token/ERC721/ERC721.sol';
import '@chainlink/contracts/src/v0.6/VRFConsumerBase.sol';
contract AdvancedCollectible is ERC721, VRFConsumerBase { // Inherit from two different contracts


    // Init vars
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    mapping (uint256 => Breed) public tokenIdToBreed;
    mapping (bytes32 => address) public requestIdToSender;
    enum Breed{WHITE, BLACK, BROWN} // New data type
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee) public // Constructor functions constructs two contracts it inherits from
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721('Kitty', 'CAT') // Token name and ticker
        {
            tokenCounter = 0;
            keyhash = _keyhash;
            fee = _fee;
        }

    function createCollectible() public returns (bytes32) { // Funtion to create token
        bytes32 requestId = requestRandomness(keyhash, fee); // Get random number
        requestIdToSender[requestId] = msg.sender; // Set mapping of request ID to the caller of the function
        emit requestedCollectible(requestId, msg.sender); // Emit event of new created token
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override { // Function to calc random number
        Breed breed = Breed(randomNumber % 3); // find breed of NFT
        uint256 newTokenId = tokenCounter; // Give token the id of the current count of tokens
        tokenIdToBreed[newTokenId] = breed; // Update mapping
        emit breedAssigned(newTokenId, breed); // emit event that mapping was updated
        address owner = requestIdToSender[requestId]; // Get owner address from mapping
        _safeMint(owner, newTokenId); // Call safe mint function
        tokenCounter++; // Increment token counter
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public { // Function to set a token URI
        require(_isApprovedOrOwner(_msgSender(), tokenId), 'ERC721: caller is not owner nor approved'); // Require the owner/approved to call function
        _setTokenURI(tokenId, _tokenURI); // Call inherited function
    }
}
