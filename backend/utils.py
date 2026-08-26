import hashlib
import os
from cryptography.fernet import Fernet
import base64


def generate_file_hash(file_path):
    """
    Generate SHA-256 hash of a file.
    
    Args:
        file_path: Path to the file to hash
        
    Returns:
        bytes32 representation of the SHA-256 hash
    """
    sha256_hash = hashlib.sha256()
    
    try:
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        # Return as bytes32 (32 bytes)
        return sha256_hash.digest()
    except Exception as e:
        print(f"Error generating file hash: {e}")
        return None


def generate_user_hash(user_id):
    """
    Generate SHA-256 hash of user ID for blockchain storage.
    
    Args:
        user_id: User identifier (email, username, etc.)
        
    Returns:
        bytes32 representation of the SHA-256 hash
    """
    sha256_hash = hashlib.sha256()
    sha256_hash.update(user_id.encode('utf-8'))
    return sha256_hash.digest()


def hash_to_hex_string(hash_bytes):
    """
    Convert bytes32 hash to hexadecimal string.
    
    Args:
        hash_bytes: bytes32 hash
        
    Returns:
        Hexadecimal string representation
    """
    if hash_bytes is None:
        return None
    return hash_bytes.hex()


def hex_string_to_hash(hex_string):
    """
    Convert hexadecimal string back to bytes32.
    
    Args:
        hex_string: Hexadecimal string
        
    Returns:
        bytes32 hash
    """
    if hex_string is None:
        return None
    return bytes.fromhex(hex_string)


def generate_encryption_key():
    """
    Generate a Fernet encryption key.
    
    Returns:
        Fernet key for encryption/decryption
    """
    return Fernet.generate_key()


def encrypt_file(file_path, key):
    """
    Encrypt a file using AES encryption.
    
    Args:
        file_path: Path to file to encrypt
        key: Fernet encryption key
        
    Returns:
        Path to encrypted file
    """
    fernet = Fernet(key)
    
    try:
        with open(file_path, 'rb') as file:
            original = file.read()
        
        encrypted = fernet.encrypt(original)
        
        encrypted_path = file_path + '.encrypted'
        with open(encrypted_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        
        return encrypted_path
    except Exception as e:
        print(f"Error encrypting file: {e}")
        return None


def decrypt_file(encrypted_path, key, output_path=None):
    """
    Decrypt a file using AES encryption.
    
    Args:
        encrypted_path: Path to encrypted file
        key: Fernet encryption key
        output_path: Path for decrypted file (optional)
        
    Returns:
        Path to decrypted file
    """
    fernet = Fernet(key)
    
    try:
        with open(encrypted_path, 'rb') as enc_file:
            encrypted = enc_file.read()
        
        decrypted = fernet.decrypt(encrypted)
        
        if output_path is None:
            output_path = encrypted_path.replace('.encrypted', '.decrypted')
        
        with open(output_path, 'wb') as dec_file:
            dec_file.write(decrypted)
        
        return output_path
    except Exception as e:
        print(f"Error decrypting file: {e}")
        return None


def verify_file_integrity(file_path, expected_hash):
    """
    Verify if a file has been tampered with by comparing hashes.
    
    Args:
        file_path: Path to file to verify
        expected_hash: Expected SHA-256 hash (bytes32)
        
    Returns:
        True if file is intact, False if tampered
    """
    current_hash = generate_file_hash(file_path)
    
    if current_hash is None:
        return False
    
    return current_hash == expected_hash


def monitor_directory_changes(directory_path):
    """
    Monitor a directory for file changes and return modified files.
    
    Args:
        directory_path: Path to directory to monitor
        
    Returns:
        List of modified file paths
    """
    modified_files = []
    
    if not os.path.exists(directory_path):
        return modified_files
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Skip encrypted files
            if not file_path.endswith('.encrypted'):
                modified_files.append(file_path)
    
    return modified_files