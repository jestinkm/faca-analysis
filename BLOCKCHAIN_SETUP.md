# Blockchain Integration Setup Guide

This guide will help you set up and test the blockchain integration for the deepfake detection system.

## Prerequisites

1. **Node.js and npm** - For smart contract compilation
2. **Python 3.8+** - For the Flask backend
3. **Ganache** or **access to Ethereum/Polygon testnet** - For blockchain deployment
4. **MetaMask** - For wallet management (optional)

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Smart Contract Development Tools

```bash
npm install -g truffle
# or
npm install -g hardhat
```

### 3. Setup Local Blockchain (Ganache)

**Option A: Using Ganache GUI**
1. Download and install [Ganache](https://trufflesuite.com/ganache/)
2. Start Ganache and note the RPC URL (usually `http://127.0.0.1:7545`)
3. Note the mnemonic phrase and account addresses

**Option B: Using Ganache CLI**
```bash
npm install -g ganache
ganache --port 7545
```

### 4. Deploy Smart Contract

**Using Truffle:**

1. Initialize Truffle in the contracts directory:
```bash
cd contracts
truffle init
```

2. Copy `AccessRecord.sol` to the `contracts/` folder

3. Create `truffle-config.js`:
```javascript
module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545,
      network_id: "*" // Match any network id
    }
  },
  compilers: {
    solc: {
      version: "0.8.0"
    }
  }
};
```

4. Create migration file `migrations/2_deploy_contracts.js`:
```javascript
const AccessRecord = artifacts.require("AccessRecord");

module.exports = function(deployer) {
  deployer.deploy(AccessRecord);
};
```

5. Deploy the contract:
```bash
truffle migrate
```

6. Note the deployed contract address

**Using Hardhat:**

1. Initialize Hardhat:
```bash
cd contracts
npx hardhat init
```

2. Copy `AccessRecord.sol` to the `contracts/` folder

3. Update `hardhat.config.js`:
```javascript
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.0",
  networks: {
    localhost: {
      url: "http://127.0.0.1:8545"
    }
  }
};
```

4. Create deployment script `scripts/deploy.js`:
```javascript
const hre = require("hardhat");

async function main() {
  const AccessRecord = await hre.ethers.getContractFactory("AccessRecord");
  const accessRecord = await AccessRecord.deploy();
  await accessRecord.deployed();
  console.log("AccessRecord deployed to:", accessRecord.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

5. Deploy the contract:
```bash
npx hardhat run scripts/deploy.js --network localhost
```

### 5. Extract Contract ABI

After deployment, find the contract ABI in:
- **Truffle**: `build/contracts/AccessRecord.json`
- **Hardhat**: `artifacts/contracts/AccessRecord.sol/AccessRecord.json`

Copy this JSON file to your project root as `contracts/AccessRecord.json`

### 6. Configure Environment Variables

Update your `.env` file with the blockchain configuration:

```bash
# Enable blockchain integration
BLOCKCHAIN_ENABLED=true

# Blockchain connection settings
BLOCKCHAIN_PROVIDER_URL=http://127.0.0.1:7545
BLOCKCHAIN_CONTRACT_ADDRESS=0x1234567890123456789012345678901234567890
BLOCKCHAIN_PRIVATE_KEY=your_private_key_from_ganache
BLOCKCHAIN_CHAIN_ID=1337
BLOCKCHAIN_CONTRACT_ABI_PATH=./contracts/AccessRecord.json

# Enable file monitoring
FILE_MONITORING_ENABLED=true

# User identifier for blockchain records
USER_ID=your_email_or_username
```

**Important:** For Ganache, the private key can be obtained from the Ganache UI or by using the mnemonic phrase with a wallet tool.

### 7. Test the Integration

Start the Flask application:

```bash
python app.py
```

## Testing API Endpoints

### 1. Check Blockchain Status
```bash
curl http://localhost:5000/api/blockchain/status
```

Expected response:
```json
{
  "enabled": true,
  "connected": true,
  "total_records": 0,
  "account_balance": 99.99
}
```

### 2. Test Face Recognition with Blockchain Recording
Use the web interface at `http://localhost:5000` - each successful/failed face recognition will now be recorded to the blockchain.

### 3. Get User Access History
```bash
curl http://localhost:5000/api/blockchain/user_history
```

### 4. Test File Integrity Verification
```bash
curl -X POST http://localhost:5000/api/blockchain/verify_file \
  -H "Content-Type: application/json" \
  -d '{"file_path": "E:\\Justin\\test_file.txt"}'
```

### 5. Test File Monitoring
```bash
# Start monitoring
curl -X POST http://localhost:5000/api/file_monitor/start

# Check status
curl http://localhost:5000/api/file_monitor/status

# Manual integrity check
curl -X POST http://localhost:5000/api/file_monitor/check

# Get monitored files
curl http://localhost:5000/api/file_monitor/files
```

## Production Deployment

### Ethereum Mainnet/Polygon

For production deployment:

1. **Update Network Configuration:**
```bash
# Polygon Mainnet
BLOCKCHAIN_PROVIDER_URL=https://polygon-rpc.com
BLOCKCHAIN_CHAIN_ID=137

# Ethereum Mainnet
BLOCKCHAIN_PROVIDER_URL=https://eth.llamarpc.com
BLOCKCHAIN_CHAIN_ID=1
```

2. **Deploy Contract to Mainnet:**
Use Truffle or Hardhat with mainnet configuration

3. **Secure Your Private Key:**
- Never commit private keys to version control
- Use environment variables or secret management services
- Consider using hardware wallets for production

4. **Fund Your Account:**
- Ensure your wallet has sufficient ETH/MATIC for gas fees

### Security Considerations

1. **Private Key Security:**
   - Use `.env` file (already in `.gitignore`)
   - Never hardcode private keys in source code
   - Use hardware wallets for high-value applications

2. **Smart Contract Security:**
   - Audit contracts before mainnet deployment
   - Consider using established contract audit services
   - Test thoroughly on testnets first

3. **Gas Optimization:**
   - Monitor gas costs
   - Consider batching transactions for high-volume scenarios
   - Use Layer 2 solutions (Polygon, Arbitrum) for lower fees

## Troubleshooting

### Connection Issues
- **Problem:** Cannot connect to blockchain
- **Solution:** Check that Ganache is running and the RPC URL is correct

### Contract Issues
- **Problem:** Contract not found
- **Solution:** Verify contract address in `.env` matches deployed contract

### Gas Issues
- **Problem:** Transactions failing due to gas
- **Solution:** Increase gas limit in blockchain_service.py or ensure account has sufficient funds

### File Monitoring Issues
- **Problem:** File monitor not working
- **Solution:** Ensure PRIVATE_FOLDER path exists and is accessible

## Next Steps

1. **Add MongoDB Integration** - Implement user authentication and face encoding storage
2. **Deepfake Detection** - Integrate CNN/LSTM models for deepfake detection
3. **File Encryption** - Implement AES encryption for sensitive files
4. **IPFS Integration** - Store encrypted files on decentralized storage

## Additional Resources

- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Solidity Documentation](https://docs.soliditylang.org/)
- [Truffle Suite](https://trufflesuite.com/)
- [Hardhat](https://hardhat.org/)
- [Polygon Documentation](https://docs.polygon.technology/)