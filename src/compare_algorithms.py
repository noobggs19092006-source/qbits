#!/usr/bin/env python3
"""
Compare Kyber-768 vs RSA-2048 Performance
"""

from oqs import KeyEncapsulation
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time
import os

def benchmark_kyber(iterations=100):
    """Benchmark Kyber-768"""
    kem = KeyEncapsulation("Kyber768")
    
    keygen_times = []
    encap_times = []
    decap_times = []
    
    print(f"   Running Kyber tests...", end='', flush=True)
    for i in range(iterations):
        if i % 20 == 0:
            print(f"\r   Running Kyber tests... {i}/{iterations}", end='', flush=True)
        
        # Key generation
        start = time.time()
        public_key = kem.generate_keypair()
        keygen_times.append((time.time() - start) * 1000)
        
        # Encapsulation
        start = time.time()
        ciphertext, shared_secret = kem.encap_secret(public_key)
        encap_times.append((time.time() - start) * 1000)
        
        # Decapsulation
        start = time.time()
        kem.decap_secret(ciphertext)
        decap_times.append((time.time() - start) * 1000)
    
    print(f"\r   Running Kyber tests... {iterations}/{iterations} ✓")
    
    return {
        'keygen': sum(keygen_times) / len(keygen_times),
        'encrypt': sum(encap_times) / len(encap_times),
        'decrypt': sum(decap_times) / len(decap_times),
        'public_key_size': len(public_key),
        'ciphertext_size': len(ciphertext)
    }

def benchmark_rsa(iterations=100):
    """Benchmark RSA-2048"""
    
    keygen_times = []
    encrypt_times = []
    decrypt_times = []
    
    data = os.urandom(32)
    
    print(f"   Running RSA tests...", end='', flush=True)
    for i in range(iterations):
        if i % 20 == 0:
            print(f"\r   Running RSA tests... {i}/{iterations}", end='', flush=True)
        
        # Key generation
        start = time.time()
        key = RSA.generate(2048)
        keygen_times.append((time.time() - start) * 1000)
        
        # Encryption
        cipher = PKCS1_OAEP.new(key.publickey())
        start = time.time()
        ciphertext = cipher.encrypt(data)
        encrypt_times.append((time.time() - start) * 1000)
        
        # Decryption
        cipher = PKCS1_OAEP.new(key)
        start = time.time()
        cipher.decrypt(ciphertext)
        decrypt_times.append((time.time() - start) * 1000)
    
    print(f"\r   Running RSA tests... {iterations}/{iterations} ✓")
    
    return {
        'keygen': sum(keygen_times) / len(keygen_times),
        'encrypt': sum(encrypt_times) / len(encrypt_times),
        'decrypt': sum(decrypt_times) / len(decrypt_times),
        'public_key_size': len(key.publickey().export_key()),
        'ciphertext_size': len(ciphertext)
    }

def main():
    print("="*70)
    print("KYBER-768 vs RSA-2048 PERFORMANCE COMPARISON")
    print("="*70)
    
    iterations = 50
    print(f"\nRunning {iterations} iterations for each algorithm...\n")
    
    # Benchmark Kyber
    kyber_results = benchmark_kyber(iterations)
    
    # Benchmark RSA
    rsa_results = benchmark_rsa(iterations)
    
    # Display results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(f"\n{'Metric':<25} {'Kyber-768':<20} {'RSA-2048':<20} {'Winner':<10}")
    print("-"*70)
    
    # Key Generation
    kyber_faster = kyber_results['keygen'] < rsa_results['keygen']
    speedup = rsa_results['keygen'] / kyber_results['keygen'] if kyber_faster else kyber_results['keygen'] / rsa_results['keygen']
    print(f"{'Key Generation':<25} {kyber_results['keygen']:>6.3f}ms          {rsa_results['keygen']:>6.3f}ms          {'Kyber' if kyber_faster else 'RSA'} ({speedup:.1f}x)")
    
    # Encryption
    kyber_faster = kyber_results['encrypt'] < rsa_results['encrypt']
    speedup = rsa_results['encrypt'] / kyber_results['encrypt'] if kyber_faster else kyber_results['encrypt'] / rsa_results['encrypt']
    print(f"{'Encryption':<25} {kyber_results['encrypt']:>6.3f}ms          {rsa_results['encrypt']:>6.3f}ms          {'Kyber' if kyber_faster else 'RSA'} ({speedup:.1f}x)")
    
    # Decryption
    kyber_faster = kyber_results['decrypt'] < rsa_results['decrypt']
    speedup = rsa_results['decrypt'] / kyber_results['decrypt'] if kyber_faster else kyber_results['decrypt'] / rsa_results['decrypt']
    print(f"{'Decryption':<25} {kyber_results['decrypt']:>6.3f}ms          {rsa_results['decrypt']:>6.3f}ms          {'Kyber' if kyber_faster else 'RSA'} ({speedup:.1f}x)")
    
    # Key Sizes
    print(f"\n{'Public Key Size':<25} {kyber_results['public_key_size']:>6} bytes       {rsa_results['public_key_size']:>6} bytes       {'Kyber' if kyber_results['public_key_size'] < rsa_results['public_key_size'] else 'RSA'}")
    
    print(f"{'Ciphertext Size':<25} {kyber_results['ciphertext_size']:>6} bytes       {rsa_results['ciphertext_size']:>6} bytes       {'Kyber' if kyber_results['ciphertext_size'] < rsa_results['ciphertext_size'] else 'RSA'}")
    
    print("\n" + "="*70)
    print("SECURITY ANALYSIS")
    print("="*70)
    print(f"{'Algorithm':<25} {'Classical Security':<25} {'Quantum Security'}")
    print("-"*70)
    print(f"{'Kyber-768':<25} {'✅ ~192 bits':<25} {'✅ SAFE'}")
    print(f"{'RSA-2048':<25} {'✅ ~112 bits':<25} {'❌ BROKEN (Shor\'s algorithm)'}")
    print("="*70)

if __name__ == "__main__":
    main()
