#!/usr/bin/env python3
"""
RSA-2048 Test for Comparison
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time
import os

def test_rsa():
    print("="*60)
    print("RSA-2048 BASIC TEST")
    print("="*60)
    
    # Generate RSA key pair
    print("\n[1] Generating RSA-2048 key pair...")
    start = time.time()
    key = RSA.generate(2048)
    keygen_time = (time.time() - start) * 1000
    print(f"✅ Key pair generated in {keygen_time:.3f}ms")
    print(f"   Public key size: {len(key.publickey().export_key())} bytes")
    print(f"   Private key size: {len(key.export_key())} bytes")
    
    # Create cipher
    cipher_rsa = PKCS1_OAEP.new(key.publickey())
    
    # Generate random data to encrypt
    data = os.urandom(32)
    print(f"\n[2] Test data: {data.hex()[:32]}...")
    
    # Encrypt
    print("\n[3] Encrypting data...")
    start = time.time()
    ciphertext = cipher_rsa.encrypt(data)
    encrypt_time = (time.time() - start) * 1000
    print(f"✅ Encryption completed in {encrypt_time:.3f}ms")
    print(f"   Ciphertext size: {len(ciphertext)} bytes")
    
    # Decrypt
    print("\n[4] Decrypting data...")
    cipher_rsa = PKCS1_OAEP.new(key)
    start = time.time()
    decrypted = cipher_rsa.decrypt(ciphertext)
    decrypt_time = (time.time() - start) * 1000
    print(f"✅ Decryption completed in {decrypt_time:.3f}ms")
    
    # Verify
    print("\n[5] Verifying decryption...")
    if data == decrypted:
        print("✅ SUCCESS! Data matches!")
    else:
        print("❌ FAILURE! Data doesn't match!")
    
    # Summary
    print("\n" + "="*60)
    print("PERFORMANCE SUMMARY")
    print("="*60)
    print(f"Key Generation:   {keygen_time:.3f}ms")
    print(f"Encryption:       {encrypt_time:.3f}ms")
    print(f"Decryption:       {decrypt_time:.3f}ms")
    print(f"Total:            {keygen_time + encrypt_time + decrypt_time:.3f}ms")
    print("="*60)

if __name__ == "__main__":
    test_rsa()
