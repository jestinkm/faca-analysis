# Polygon Testnet Setup Guide

This guide will help you set up free blockchain access using Polygon Mumbai testnet for your deepfake detection system.

## 🌐 Why Polygon Mumbai Testnet?

- **Free**: No real money required
- **Fast**: Quick transaction confirmations
- **Compatible**: Ethereum-compatible tools
- **Easy**: Simple setup process
- **Testnet**: Perfect for development and testing

## 🚀 Setup Steps

### 1. Install MetaMask

1. Download [MetaMask](https://metamask.io/download/)
2. Install as browser extension (Chrome, Firefox, Brave, etc.)
3. Create a new wallet
4. **IMPORTANT**: Save your seed phrase securely (never share it!)
5. Set a strong password

### 2. Add Polygon Mumbai Testnet to MetaMask

#### Option A: Automatic Addition

1. Go to [Polygon Network](https://polygon.technology/)
2. Click "Add Polygon Network" 
3. Approve the MetaMask popup
4. Switch to "Mumbai Testnet" in MetaMask

#### Option B: Manual Addition

1. Open MetaMask
2. Click network dropdown → "Add Network" → "Add a network manually"
3. Enter these details:

**Network Name**: `Polygon Mumbai Testnet`

**RPC URL**: `https://rpc-mumbai.polygon.technology/`

**Chain ID**: `80001` (or `137` in decimal)

**Currency Symbol**: `MATIC`

**Block Explorer URL**: `https://mumbai.polygonscan.com/`

4. Click "Save"

### 3. Get Free Test MATIC Tokens

#### Method 1: Polygon Faucet (Recommended)

1. Go to [Polygon Mumbai Faucet](https://faucet.polygon.technology/)
2. Connect your MetaMask wallet
3. Ensure you're on Mumbai Testnet
4. Request test MATIC (usually 0.1-1 MATIC)
5. Wait for transaction confirmation (1-2 minutes)

#### Method 2: Quick Faucet

1. Go to [Quick Faucet](https://faucet.quicknode.com/polygon/mumbai)
2. Enter your wallet address
3. Complete captcha if required
4. Request test MATIC

#### Method 3: Alchemy Faucet

1. Go to [Alchemy Faucet](https://goerlifaucet.com/)
2. Select Polygon Mumbai
3. Enter your wallet address
4. Request test tokens

### 4. Deploy Smart Contract to Mumbai

#### Using Remix IDE (Easiest)

1. Go to [Remix IDE](https://remix.ethereum.org/)
2. Create new file: `AccessRecord.sol`
3. Copy your contract code from `contracts/AccessRecord.sol`
4. Paste into Remix editor

#### Compile Contract

1. Click "Solidity Compiler" tab (left sidebar)
2. Select compiler version: `0.8.0` (or match your pragma)
3. Click "Compile AccessRecord.sol"
4. Wait for compilation (green checkmark)

#### Deploy Contract

1. Click "Deploy & Run Transactions" tab
2. Select environment: "Injected Provider - MetaMask"
3. MetaMask popup will appear - approve connection
4. Ensure you're on Mumbai Testnet in MetaMask
5. Select "AccessRecord" from contract dropdown
6. Click "Deploy"
7. MetaMask popup will appear - confirm transaction
8. Wait for deployment (30-60 seconds)
9. Copy the deployed contract address (bottom of deployed contracts)

#### Save Contract Information

Save these details somewhere safe:

```
Contract Address: 0x1234567890123456789012345678901234567890
Network: Polygon Mumbai Testnet
Transaction Hash: 0xabc...
```

### 5. Get Contract ABI

#### From Remix

1. In Remix, go to "Solidity Compiler" tab
2. Click "Compilation Details" (button next to Compile)
3. Scroll down to "ABI" section
4. Copy the entire ABI JSON

#### Save ABI

Create a file `contracts/AccessRecord.json` and paste the ABI:

```json
{
  "abi": [
    // Paste the ABI here
  ]
}
```

Alternatively, update the `CONTRACT_ABI` in `backend/contract_abi.py`:

```python
CONTRACT_ABI = [
    # Paste the ABI array here
]
```

### 6. Update Environment Variables

Add these to your `.env` file:

```bash
# Blockchain Configuration
BLOCKCHAIN_ENABLED=true
BLOCKCHAIN_PROVIDER_URL=https://rpc-mumbai.polygon.technology/
BLOCKCHAIN_CONTRACT_ADDRESS=0xYourDeployedContractAddress
BLOCKCHAIN_PRIVATE_KEY=your_metamask_private_key
BLOCKCHAIN_CHAIN_ID=80001
BLOCKCHAIN_CONTRACT_ABI_PATH=./contracts/AccessRecord.json
```

#### Getting Your Private Key from MetaMask

1. Open MetaMask
2. Click account icon → "Account Details"
3. Click "Export Private Key"
4. Enter your MetaMask password
5. Copy the private key (starts with 0x...)
6. **WARNING**: Never share this key!

### 7. Test Blockchain Connection

Create a test script:

```python
# test_blockchain.py
import os
from dotenv import load_dotenv
from blockchain_service import create_blockchain_service_from_env

load_dotenv()

try:
    blockchain = create_blockchain_service_from_env()
    
    if blockchain and blockchain.is_connected():
        print("✅ Blockchain connection successful!")
        print(f"Chain ID: {blockchain.chain_id}")
        print(f"Contract Address: {blockchain.contract_address}")
        print(f"Account: {blockchain.account.address if blockchain.account else 'N/A'}")
        print(f"Balance: {blockchain.get_account_balance()} MATIC")
        print(f"Total Records: {blockchain.get_total_records()}")
    else:
        print("❌ Blockchain connection failed")
        
except Exception as e:
    print(f"❌ Error: {e}")
```

Run: `python test_blockchain.py`

### 8. Test Smart Contract Interaction

```python
# test_contract.py
import os
from dotenv import load_dotenv
from blockchain_service import create_blockchain_service_from_env
from utils import generate_user_hash

load_dotenv()

try:
    blockchain = create_blockchain_service_from_env()
    
    # Test recording access
    user_id = "test@example.com"
    tx_hash = blockchain.record_access(
        user_id=user_id,
        file_path=None,
        granted=True,
        access_type="TEST"
    )
    
    if tx_hash:
        print(f"✅ Test transaction successful: {tx_hash}")
        
        # Verify on PolygonScan
        print(f"View on PolygonScan: https://mumbai.polygonscan.com/tx/{tx_hash}")
    else:
        print("❌ Transaction failed")
        
except Exception as e:
    print(f"❌ Error: {e}")
```

## 🔍 Monitor on PolygonScan

1. Go to [PolygonScan Mumbai](https://mumbai.polygonscan.com/)
2. Search your contract address
3. View transactions, contract code, and events
4. Monitor gas usage and costs

## ⛽ Gas Fees on Testnet

- **Cost**: Free (test tokens)
- **Gas Price**: Very low compared to mainnet
- **Confirmation Time**: 5-30 seconds
- **Refill**: Get more tokens from faucet when needed

## 🔄 Contract Management

### Updating Contract

If you need to update the contract:

1. Make changes to `AccessRecord.sol`
2. Deploy new contract (gets new address)
3. Update `BLOCKCHAIN_CONTRACT_ADDRESS` in `.env`
4. Migrate data if needed (not automatic)

### Contract Verification

1. Go to PolygonScan
2. Search your contract address
3. Click "Verify and Publish"
4. Select compiler type and version
5. Paste contract source code
6. Submit for verification

## 🚨 Troubleshooting

### MetaMask Issues

**Problem**: "Network not added to MetaMask"
- **Solution**: Use the manual addition steps above

**Problem**: "Insufficient funds"
- **Solution**: Get more test MATIC from faucet

**Problem**: "Transaction failed"
- **Solution**: Check gas price, ensure sufficient MATIC

### Contract Deployment Issues

**Problem**: "Compilation error"
- **Solution**: Check Solidity version matches pragma

**Problem**: "Deployment timeout"
- **Solution**: Check network connection, try again

**Problem**: "Out of gas"
- **Solution**: Increase gas limit in deployment settings

### Backend Integration Issues

**Problem**: "Connection refused"
- **Solution**: Check RPC URL, ensure Mumbai testnet

**Problem**: "Contract not found"
- **Solution**: Verify contract address is correct

**Problem**: "Invalid ABI"
- **Solution**: Ensure ABI matches deployed contract

## 🛡️ Security Best Practices

1. **Never share private keys** or seed phrases
2. **Use testnet only** for development
3. **Verify contract addresses** before transactions
4. **Monitor test token usage** to avoid running out
5. **Keep MetaMask updated** to latest version

## 📊 Testnet vs Mainnet

| Feature | Testnet (Mumbai) | Mainnet (Polygon) |
|---------|------------------|-------------------|
| Cost | Free | Real MATIC |
| Purpose | Development | Production |
| Security | Lower | Higher |
| Speed | Fast | Fast |
| Tools | Same | Same |

## 🎯 Production Migration

When ready for mainnet:

1. **Deploy to Polygon Mainnet**
2. **Get real MATIC tokens**
3. **Update environment variables**:
   - `BLOCKCHAIN_PROVIDER_URL=https://polygon-rpc.com/`
   - `BLOCKCHAIN_CHAIN_ID=137`
4. **Deploy new contract** to mainnet
5. **Test thoroughly** with small amounts
6. **Monitor gas costs** on mainnet

## 📈 Alternative Testnets

If Mumbai has issues:

### Goerli (Ethereum Testnet)
- **RPC**: `https://goerli.infura.io/v3/YOUR_INFURA_KEY`
- **Chain ID**: 5
- **Faucet**: [Goerli Faucet](https://goerlifaucet.com/)

### Sepolia (Ethereum Testnet)
- **RPC**: `https://rpc.sepolia.org/`
- **Chain ID**: 11155111
- **Faucet**: [Sepolia Faucet](https://sepoliafaucet.com/)

## 🎉 Next Steps

1. ✅ MetaMask installed and configured
2. ✅ Polygon Mumbai testnet added
3. ✅ Test MATIC tokens obtained
4. ✅ Smart contract deployed
5. ✅ Contract ABI obtained
6. ✅ Environment variables updated
7. ✅ Blockchain connection tested
8. ✅ Contract interaction tested

Your blockchain integration is now ready for testing with free Polygon Mumbai testnet!