SWAP_CONTRACT_ABI = '''
[
  {
    "inputs": [
      {
        "internalType": "contract IERC20",
        "name": "_tokenAddress",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_feeAddress",
        "type": "address"
      },
      {
        "internalType": "uint128",
        "name": "__numOfTotalBlockchains",
        "type": "uint128"
      },
      {
        "internalType": "uint128",
        "name": "__numOfThisBlockchain",
        "type": "uint128"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "previousOwner",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "OwnershipTransferred",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "TransferFromOtherBlockchain",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint128",
        "name": "blockchain",
        "type": "uint128"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "newAddress",
        "type": "string"
      }
    ],
    "name": "TransferToOtherBlockchain",
    "type": "event"
  },
  {
    "inputs": [
      {
        "internalType": "uint128",
        "name": "newNumOfThisBlockchain",
        "type": "uint128"
      },
      {
        "internalType": "uint128",
        "name": "newNumOfTotalBlockchains",
        "type": "uint128"
      }
    ],
    "name": "changeInformationAboutOtherBlockchain",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "feeAddress",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "renounceOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "tokenAddress",
    "outputs": [
      {
        "internalType": "contract IERC20",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "transferOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint128",
        "name": "blockchain",
        "type": "uint128"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "newAddress",
        "type": "string"
      }
    ],
    "name": "transferToOtherBlockchain",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amountToUser",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "feeAmount",
        "type": "uint256"
      }
    ],
    "name": "transferToUserWithFee",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "transferToUserWithoutFee",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
'''