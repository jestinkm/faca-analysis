# Contract ABI for AccessRecord smart contract
# Replace this with your actual contract ABI after deployment
CONTRACT_ABI = [
    {
        "inputs": [],
        "name": "getTotalRecords",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "_userHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "_fileHash", "type": "bytes32"},
            {"internalType": "bool", "name": "_granted", "type": "bool"},
            {"internalType": "string", "name": "_accessType", "type": "string"}
        ],
        "name": "recordAccess",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_recordId", "type": "uint256"}],
        "name": "getAccessRecord",
        "outputs": [
            {"internalType": "bytes32", "name": "userHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "fileHash", "type": "bytes32"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
            {"internalType": "bool", "name": "granted", "type": "bool"},
            {"internalType": "string", "name": "accessType", "type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "_userHash", "type": "bytes32"}],
        "name": "getUserAccessHistory",
        "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "_userHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "_currentFileHash", "type": "bytes32"}
        ],
        "name": "verifyFileIntegrity",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]