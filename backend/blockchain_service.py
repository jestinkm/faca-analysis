from web3 import Web3
try:
    from web3.middleware import ExtraDataPOAMiddleware
    HAS_POA_MIDDLEWARE = True
except ImportError:
    # Fallback for older web3 versions
    try:
        from web3.middleware import geth_poa_middleware
        HAS_POA_MIDDLEWARE = True
    except ImportError:
        HAS_POA_MIDDLEWARE = False
import json
import os
from typing import Optional, Dict, Any
import logging
from utils import generate_user_hash, generate_file_hash, hash_to_hex_string

# Try to import contract ABI from Python file for cloud deployment
try:
    from contract_abi import CONTRACT_ABI
    HAS_CONTRACT_ABI_MODULE = True
except ImportError:
    HAS_CONTRACT_ABI_MODULE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BlockchainService:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize blockchain service with configuration.
        
        Args:
            config: Dictionary containing blockchain configuration
                   - provider_url: RPC endpoint URL
                   - contract_address: Deployed contract address
                   - contract_abi: Contract ABI
                   - private_key: Wallet private key (for transactions)
                   - chain_id: Blockchain network chain ID
        """
        self.provider_url = config.get('provider_url')
        self.contract_address = config.get('contract_address')
        self.contract_abi = config.get('contract_abi')
        self.private_key = config.get('private_key')
        self.chain_id = config.get('chain_id', 1)
        
        # Initialize Web3 connection
        self.w3 = self._connect_to_blockchain()
        self.contract = self._load_contract()
        self.account = self._load_account()
        
        logger.info(f"Blockchain service initialized on chain {self.chain_id}")

    def _connect_to_blockchain(self) -> Web3:
        """Establish connection to blockchain network."""
        try:
            w3 = Web3(Web3.HTTPProvider(self.provider_url))
            
            # Add POA middleware for testnets like Polygon
            if self.chain_id in [137, 80001, 5]:  # Polygon, Mumbai, Goerli
                if HAS_POA_MIDDLEWARE:
                    try:
                        # web3.py v7 uses ExtraDataPOAMiddleware
                        w3.middleware_onion.inject(ExtraDataPOAMiddleware, layer=0)
                    except NameError:
                        # Fallback for older web3 versions
                        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            if not w3.is_connected():
                raise ConnectionError("Failed to connect to blockchain")
            
            logger.info(f"Connected to blockchain. Block: {w3.eth.block_number}")
            return w3
        except Exception as e:
            logger.error(f"Blockchain connection error: {e}")
            raise

    def _load_contract(self):
        """Load smart contract instance."""
        try:
            if not self.contract_address:
                logger.warning("Contract address not provided")
                return None
            
            # Use embedded ABI if available, otherwise try to load from file
            abi = self.contract_abi
            if not abi and HAS_CONTRACT_ABI_MODULE:
                logger.info("Using embedded contract ABI")
                abi = CONTRACT_ABI
            elif not abi:
                logger.warning("Contract ABI not provided")
                return None
            
            contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(self.contract_address),
                abi=abi
            )
            logger.info(f"Contract loaded at {self.contract_address}")
            return contract
        except Exception as e:
            logger.error(f"Contract loading error: {e}")
            return None

    def _load_account(self):
        """Load wallet account from private key."""
        try:
            if not self.private_key:
                logger.warning("Private key not provided - read-only mode")
                return None
            
            account = self.w3.eth.account.from_key(self.private_key)
            logger.info(f"Account loaded: {account.address}")
            return account
        except Exception as e:
            logger.error(f"Account loading error: {e}")
            return None

    def record_access(self, user_id: str, file_path: Optional[str] = None, 
                     granted: bool = True, access_type: str = "LOGIN") -> Optional[str]:
        """
        Record access attempt to blockchain.
        
        Args:
            user_id: User identifier (email, username, etc.)
            file_path: Path to accessed file (optional)
            granted: Whether access was granted
            access_type: Type of access ("LOGIN", "FILE_ACCESS", "FILE_TAMPER")
            
        Returns:
            Transaction hash if successful, None otherwise
        """
        try:
            if not self.contract or not self.account:
                logger.error("Contract or account not available")
                return None
            
            # Generate hashes
            user_hash = generate_user_hash(user_id)
            file_hash = generate_file_hash(file_path) if file_path else b'\x00' * 32
            
            # Build transaction
            transaction = self.contract.functions.recordAccess(
                user_hash,
                file_hash,
                granted,
                access_type
            ).build_transaction({
                'from': self.account.address,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'chainId': self.chain_id
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Wait for transaction receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            if receipt.status == 1:
                logger.info(f"Access recorded successfully. TX: {tx_hash.hex()}")
                return tx_hash.hex()
            else:
                logger.error("Transaction failed")
                return None
                
        except Exception as e:
            logger.error(f"Error recording access: {e}")
            return None

    def get_access_record(self, record_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve access record from blockchain.
        
        Args:
            record_id: ID of the access record
            
        Returns:
            Dictionary containing access record data
        """
        try:
            if not self.contract:
                logger.error("Contract not available")
                return None
            
            record = self.contract.functions.getAccessRecord(record_id).call()
            
            return {
                'user_hash': hash_to_hex_string(record[0]),
                'file_hash': hash_to_hex_string(record[1]),
                'timestamp': record[2],
                'granted': record[3],
                'access_type': record[4]
            }
        except Exception as e:
            logger.error(f"Error retrieving access record: {e}")
            return None

    def get_user_history(self, user_id: str) -> list:
        """
        Get access history for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of record IDs for the user
        """
        try:
            if not self.contract:
                logger.error("Contract not available")
                return []
            
            user_hash = generate_user_hash(user_id)
            record_ids = self.contract.functions.getUserAccessHistory(user_hash).call()
            
            return record_ids
        except Exception as e:
            logger.error(f"Error retrieving user history: {e}")
            return []

    def verify_file_integrity(self, user_id: str, file_path: str) -> bool:
        """
        Verify file integrity against blockchain records.
        
        Args:
            user_id: User identifier
            file_path: Path to file to verify
            
        Returns:
            True if file is intact, False if tampered
        """
        try:
            if not self.contract:
                logger.error("Contract not available")
                return False
            
            user_hash = generate_user_hash(user_id)
            current_file_hash = generate_file_hash(file_path)
            
            if current_file_hash is None:
                return False
            
            is_valid = self.contract.functions.verifyFileIntegrity(
                user_hash, current_file_hash
            ).call()
            
            logger.info(f"File integrity check: {is_valid}")
            return is_valid
        except Exception as e:
            logger.error(f"Error verifying file integrity: {e}")
            return False

    def get_total_records(self) -> int:
        """Get total number of access records on blockchain."""
        try:
            if not self.contract:
                return 0
            
            return self.contract.functions.getTotalRecords().call()
        except Exception as e:
            logger.error(f"Error getting total records: {e}")
            return 0

    def is_connected(self) -> bool:
        """Check if blockchain connection is active."""
        return self.w3.is_connected() if self.w3 else False

    def get_account_balance(self) -> Optional[float]:
        """Get account balance in ETH."""
        try:
            if not self.account:
                return None
            
            balance_wei = self.w3.eth.get_balance(self.account.address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return float(balance_eth)
        except Exception as e:
            logger.error(f"Error getting account balance: {e}")
            return None


def load_contract_abi(contract_path: str) -> list:
    """
    Load contract ABI from JSON file.
    
    Args:
        contract_path: Path to contract JSON file
        
    Returns:
        Contract ABI as list
    """
    try:
        with open(contract_path, 'r') as f:
            contract_data = json.load(f)
            return contract_data['abi']
    except Exception as e:
        logger.error(f"Error loading contract ABI: {e}")
        return []


def create_blockchain_service_from_env() -> BlockchainService:
    """
    Create blockchain service instance from environment variables.
    
    Expected environment variables:
    - BLOCKCHAIN_PROVIDER_URL
    - BLOCKCHAIN_CONTRACT_ADDRESS  
    - BLOCKCHAIN_PRIVATE_KEY
    - BLOCKCHAIN_CHAIN_ID
    - BLOCKCHAIN_CONTRACT_ABI_PATH
    """
    config = {
        'provider_url': os.getenv('BLOCKCHAIN_PROVIDER_URL', 'http://localhost:8545'),
        'contract_address': os.getenv('BLOCKCHAIN_CONTRACT_ADDRESS'),
        'private_key': os.getenv('BLOCKCHAIN_PRIVATE_KEY'),
        'chain_id': int(os.getenv('BLOCKCHAIN_CHAIN_ID', '1337')),
        'contract_abi': None
    }
    
    # Load ABI from file if path provided
    abi_path = os.getenv('BLOCKCHAIN_CONTRACT_ABI_PATH')
    if abi_path and os.path.exists(abi_path):
        config['contract_abi'] = load_contract_abi(abi_path)
    
    return BlockchainService(config)