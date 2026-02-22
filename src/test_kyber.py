#!/usr/bin/env python3
"""
Basic Kyber-768 Test
Tests key generation, encapsulation, and decapsulation
"""

from oqs import KeyEncapsulation
import time
import sys

def test_kyber():
    print("="*60)
    print("KYBER-768 BASIC TEST")
    print("="*60)
    
    # Initialize Kyber-768
    print("\n[1] Initializing Kyber-768...")
    kem = KeyEncapsulation("Kyber768")
    print("✅ Kyber-768 initialized")
    
    # Generate key pair
    print("\n[2] Generating key pair...")
    start = time.time()
    public_key = kem.generate_keypair()
    keygen_time = (time.time() - start) * 1000
    print(f"✅ Key pair generated in {keygen_time:.3f}ms")
    print(f"   Public key size: {len(public_key)} bytes")
    print(f"   Secret key size: {len(kem.export_secret_key())} bytes")
    
    # Encapsulation (sender side)
    print("\n[3] Encapsulating shared secret...")
    start = time.time()
    ciphertext, shared_secret_sender = kem.encap_secret(public_key)
    encap_time = (time.time() - start) * 1000
    print(f"✅ Encapsulation completed in {encap_time:.3f}ms")
    print(f"   Ciphertext size: {len(ciphertext)} bytes")
    print(f"   Shared secret: {shared_secret_sender.hex()[:32]}...")
    
    # Decapsulation (receiver side)
    print("\n[4] Decapsulating shared secret...")
    start = time.time()
    shared_secret_receiver = kem.decap_secret(ciphertext)
    decap_time = (time.time() - start) * 1000
    print(f"✅ Decapsulation completed in {decap_time:.3f}ms")
    print(f"   Shared secret: {shared_secret_receiver.hex()[:32]}...")
    
    # Verify secrets match
    print("\n[5] Verifying shared secrets match...")
    if shared_secret_sender == shared_secret_receiver:
        print("✅ SUCCESS! Shared secrets match!")
        print(f"   Secret length: {len(shared_secret_sender)} bytes")
    else:
        print("❌ FAILURE! Secrets don't match!")
        sys.exit(1)
    
    # Summary
    print("\n" + "="*60)
    print("PERFORMANCE SUMMARY")
    print("="*60)
    print(f"Key Generation:   {keygen_time:.3f}ms")
    print(f"Encapsulation:    {encap_time:.3f}ms")
    print(f"Decapsulation:    {decap_time:.3f}ms")
    print(f"Total:            {keygen_time + encap_time + decap_time:.3f}ms")
    print("="*60)

if __name__ == "__main__":
    test_kyber()
