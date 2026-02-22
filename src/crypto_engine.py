#!/usr/bin/env python3
"""
Quantum-Resistant Cryptography Engine
Supports: Kyber-768, RSA-2048, and Hybrid mode
"""

from oqs import KeyEncapsulation
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import os
import json
import base64
import time

class CryptoEngine:
    """Main cryptography engine supporting multiple algorithms"""
    
    ALGORITHMS = ['kyber768', 'rsa2048', 'hybrid']
    
    def __init__(self, algorithm='kyber768'):
        if algorithm not in self.ALGORITHMS:
            raise ValueError(f"Algorithm must be one of {self.ALGORITHMS}")
        self.algorithm = algorithm
        self.kyber_kem = None
        self.rsa_key = None
        
    def generate_keys(self):
        """Generate key pair based on selected algorithm"""
        start_time = time.time()
        keys = {}
        
        if self.algorithm in ['kyber768', 'hybrid']:
            # Generate Kyber keys
            self.kyber_kem = KeyEncapsulation("Kyber768")
            kyber_public = self.kyber_kem.generate_keypair()
            kyber_secret = self.kyber_kem.export_secret_key()
            
            keys['kyber_public'] = base64.b64encode(kyber_public).decode()
            keys['kyber_secret'] = base64.b64encode(kyber_secret).decode()
        
        if self.algorithm in ['rsa2048', 'hybrid']:
            # Generate RSA keys
            self.rsa_key = RSA.generate(2048)
            rsa_public = self.rsa_key.publickey().export_key()
            rsa_private = self.rsa_key.export_key()
            
            keys['rsa_public'] = base64.b64encode(rsa_public).decode()
            keys['rsa_private'] = base64.b64encode(rsa_private).decode()
        
        keys['algorithm'] = self.algorithm
        keys['generation_time'] = time.time() - start_time
        
        return keys
    
    def encrypt_data(self, data, public_keys):
        """
        Encrypt data using selected algorithm
        Returns: (ciphertext, metadata)
        """
        start_time = time.time()
        
        if isinstance(data, str):
            data = data.encode()
        
        # Generate random AES key
        aes_key = get_random_bytes(32)  # 256-bit key
        
        # Encrypt data with AES
        cipher_aes = AES.new(aes_key, AES.MODE_GCM)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        
        result = {
            'algorithm': self.algorithm,
            'nonce': base64.b64encode(cipher_aes.nonce).decode(),
            'tag': base64.b64encode(tag).decode(),
            'ciphertext': base64.b64encode(ciphertext).decode()
        }
        
        if self.algorithm == 'kyber768':
            # Encapsulate AES key with Kyber
            kyber_public = base64.b64decode(public_keys['kyber_public'])
            kem = KeyEncapsulation("Kyber768")
            kyber_ciphertext, shared_secret = kem.encap_secret(kyber_public)
            
            # Derive AES key from shared secret
            derived_key = PBKDF2(shared_secret, b'kyber', dkLen=32)
            
            # Re-encrypt AES key with derived key
            cipher = AES.new(derived_key, AES.MODE_GCM)
            encrypted_aes_key, key_tag = cipher.encrypt_and_digest(aes_key)
            
            result['kyber_ciphertext'] = base64.b64encode(kyber_ciphertext).decode()
            result['key_nonce'] = base64.b64encode(cipher.nonce).decode()
            result['key_tag'] = base64.b64encode(key_tag).decode()
            result['encrypted_key'] = base64.b64encode(encrypted_aes_key).decode()
            
        elif self.algorithm == 'rsa2048':
            # Encrypt AES key with RSA
            rsa_public = RSA.import_key(base64.b64decode(public_keys['rsa_public']))
            cipher_rsa = PKCS1_OAEP.new(rsa_public)
            encrypted_aes_key = cipher_rsa.encrypt(aes_key)
            
            result['encrypted_key'] = base64.b64encode(encrypted_aes_key).decode()
            
        elif self.algorithm == 'hybrid':
            # Use both Kyber and RSA
            # Kyber part
            kyber_public = base64.b64decode(public_keys['kyber_public'])
            kem = KeyEncapsulation("Kyber768")
            kyber_ciphertext, kyber_secret = kem.encap_secret(kyber_public)
            
            # RSA part - encrypt half the AES key
            rsa_public = RSA.import_key(base64.b64decode(public_keys['rsa_public']))
            cipher_rsa = PKCS1_OAEP.new(rsa_public)
            # Split AES key: first 16 bytes with RSA, derive rest from Kyber
            rsa_encrypted_key = cipher_rsa.encrypt(aes_key[:16])
            
            # Derive the wrapping key from Kyber secret
            wrapping_key = PBKDF2(kyber_secret, b'hybrid', dkLen=32)
            
            # Encrypt the full AES key with the wrapping key
            cipher = AES.new(wrapping_key, AES.MODE_GCM)
            encrypted_aes_key, key_tag = cipher.encrypt_and_digest(aes_key)
            
            result['kyber_ciphertext'] = base64.b64encode(kyber_ciphertext).decode()
            result['rsa_encrypted'] = base64.b64encode(rsa_encrypted_key).decode()
            result['key_nonce'] = base64.b64encode(cipher.nonce).decode()
            result['key_tag'] = base64.b64encode(key_tag).decode()
            result['encrypted_key'] = base64.b64encode(encrypted_aes_key).decode()
        
        result['encryption_time'] = time.time() - start_time
        return result
    
    def decrypt_data(self, encrypted_data, private_keys):
        """
        Decrypt data using selected algorithm
        Returns: original data
        """
        start_time = time.time()
        
        algorithm = encrypted_data['algorithm']
        
        if algorithm == 'kyber768':
            # Decapsulate with Kyber
            kyber_secret = base64.b64decode(private_keys['kyber_secret'])
            kyber_ciphertext = base64.b64decode(encrypted_data['kyber_ciphertext'])
            
            kem = KeyEncapsulation("Kyber768", kyber_secret)
            shared_secret = kem.decap_secret(kyber_ciphertext)
            
            # Derive key
            derived_key = PBKDF2(shared_secret, b'kyber', dkLen=32)
            
            # Decrypt AES key
            cipher = AES.new(derived_key, AES.MODE_GCM, nonce=base64.b64decode(encrypted_data['key_nonce']))
            aes_key = cipher.decrypt_and_verify(
                base64.b64decode(encrypted_data['encrypted_key']),
                base64.b64decode(encrypted_data['key_tag'])
            )
            
        elif algorithm == 'rsa2048':
            # Decrypt with RSA
            rsa_private = RSA.import_key(base64.b64decode(private_keys['rsa_private']))
            cipher_rsa = PKCS1_OAEP.new(rsa_private)
            aes_key = cipher_rsa.decrypt(base64.b64decode(encrypted_data['encrypted_key']))
            
        elif algorithm == 'hybrid':
            # Decrypt with both
            # Get Kyber shared secret
            kyber_secret = base64.b64decode(private_keys['kyber_secret'])
            kyber_ciphertext = base64.b64decode(encrypted_data['kyber_ciphertext'])
            
            kem = KeyEncapsulation("Kyber768", kyber_secret)
            kyber_shared = kem.decap_secret(kyber_ciphertext)
            
            # Derive wrapping key from Kyber secret
            wrapping_key = PBKDF2(kyber_shared, b'hybrid', dkLen=32)
            
            # Decrypt the full AES key
            cipher = AES.new(wrapping_key, AES.MODE_GCM, nonce=base64.b64decode(encrypted_data['key_nonce']))
            aes_key = cipher.decrypt_and_verify(
                base64.b64decode(encrypted_data['encrypted_key']),
                base64.b64decode(encrypted_data['key_tag'])
            )
            
            # Verify RSA part (optional check for double security)
            rsa_private = RSA.import_key(base64.b64decode(private_keys['rsa_private']))
            cipher_rsa = PKCS1_OAEP.new(rsa_private)
            rsa_part = cipher_rsa.decrypt(base64.b64decode(encrypted_data['rsa_encrypted']))
            
            # Verify first 16 bytes match
            if aes_key[:16] != rsa_part:
                raise ValueError("Hybrid decryption failed: RSA and Kyber parts don't match")
        
        # Decrypt actual data with AES
        cipher_aes = AES.new(aes_key, AES.MODE_GCM, nonce=base64.b64decode(encrypted_data['nonce']))
        plaintext = cipher_aes.decrypt_and_verify(
            base64.b64decode(encrypted_data['ciphertext']),
            base64.b64decode(encrypted_data['tag'])
        )
        
        return plaintext

def test_crypto_engine():
    """Test all three modes"""
    print("="*70)
    print("CRYPTO ENGINE TEST")
    print("="*70)
    
    test_data = b"This is a secret message that needs quantum-safe protection!"
    
    for algorithm in CryptoEngine.ALGORITHMS:
        print(f"\n{'='*70}")
        print(f"Testing: {algorithm.upper()}")
        print('='*70)
        
        # Initialize
        engine = CryptoEngine(algorithm)
        
        # Generate keys
        print("Generating keys...")
        keys = engine.generate_keys()
        print(f"✅ Keys generated in {keys['generation_time']*1000:.3f}ms")
        
        # Encrypt
        print("Encrypting data...")
        encrypted = engine.encrypt_data(test_data, keys)
        print(f"✅ Data encrypted in {encrypted['encryption_time']*1000:.3f}ms")
        print(f"   Original size: {len(test_data)} bytes")
        print(f"   Encrypted size: {len(base64.b64decode(encrypted['ciphertext']))} bytes")
        
        # Decrypt
        print("Decrypting data...")
        start = time.time()
        decrypted = engine.decrypt_data(encrypted, keys)
        decrypt_time = time.time() - start
        print(f"✅ Data decrypted in {decrypt_time*1000:.3f}ms")
        
        # Verify
        if decrypted == test_data:
            print("✅ SUCCESS! Data matches!")
        else:
            print("❌ FAILURE! Data doesn't match!")
            
    print("\n" + "="*70)
    print("ALL TESTS COMPLETED")
    print("="*70)

if __name__ == "__main__":
    test_crypto_engine()
