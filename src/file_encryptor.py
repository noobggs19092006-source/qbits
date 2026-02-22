#!/usr/bin/env python3
"""
File Encryption System
Encrypts and decrypts files using quantum-safe algorithms
"""

import os
import json
import time
from pathlib import Path
from crypto_engine import CryptoEngine

class FileEncryptor:
    """Handle file encryption and decryption"""
    
    def __init__(self, algorithm='kyber768'):
        self.engine = CryptoEngine(algorithm)
        self.keys = None
        
    def generate_keys(self, save_to=None):
        """Generate and optionally save keys"""
        self.keys = self.engine.generate_keys()
        
        if save_to:
            # Save keys to files
            public_key_file = Path(save_to) / 'public_key.json'
            private_key_file = Path(save_to) / 'private_key.json'
            
            # Separate public and private keys
            public_keys = {}
            private_keys = {}
            
            for key, value in self.keys.items():
                if 'public' in key or key == 'algorithm':
                    public_keys[key] = value
                elif 'private' in key or 'secret' in key:
                    private_keys[key] = value
            
            # Save public keys
            with open(public_key_file, 'w') as f:
                json.dump(public_keys, f, indent=2)
            
            # Save private keys (with warning)
            with open(private_key_file, 'w') as f:
                json.dump(private_keys, f, indent=2)
            
            # Set restrictive permissions on private key
            os.chmod(private_key_file, 0o600)
            
            print(f"✅ Keys saved to {save_to}")
            print(f"   Public key:  {public_key_file}")
            print(f"   Private key: {private_key_file} (keep this secret!)")
        
        return self.keys
    
    def load_keys(self, keys_dir):
        """Load keys from directory"""
        public_key_file = Path(keys_dir) / 'public_key.json'
        private_key_file = Path(keys_dir) / 'private_key.json'
        
        self.keys = {}
        
        # Load public keys
        if public_key_file.exists():
            with open(public_key_file, 'r') as f:
                self.keys.update(json.load(f))
        
        # Load private keys
        if private_key_file.exists():
            with open(private_key_file, 'r') as f:
                self.keys.update(json.load(f))
        
        return self.keys
    
    def encrypt_file(self, input_file, output_file=None):
        """
        Encrypt a file
        Returns: (output_file_path, metadata)
        """
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Default output file
        if output_file is None:
            output_file = str(input_path) + '.encrypted'
        
        print(f"📄 Encrypting: {input_path.name}")
        print(f"   Size: {input_path.stat().st_size:,} bytes")
        
        # Read file
        start_time = time.time()
        with open(input_path, 'rb') as f:
            data = f.read()
        read_time = time.time() - start_time
        
        # Encrypt
        print(f"   🔒 Encrypting with {self.keys['algorithm']}...")
        encrypted = self.engine.encrypt_data(data, self.keys)
        
        # Add file metadata
        encrypted['original_filename'] = input_path.name
        encrypted['original_size'] = len(data)
        encrypted['encrypted_at'] = time.time()
        
        # Save encrypted file
        start_time = time.time()
        with open(output_file, 'w') as f:
            json.dump(encrypted, f, indent=2)
        write_time = time.time() - start_time
        
        output_size = Path(output_file).stat().st_size
        
        print(f"   ✅ Encrypted in {encrypted['encryption_time']*1000:.2f}ms")
        print(f"   💾 Output: {output_file}")
        print(f"   📊 Size: {output_size:,} bytes (overhead: {((output_size/len(data))-1)*100:.1f}%)")
        
        return output_file, encrypted
    
    def decrypt_file(self, input_file, output_file=None):
        """
        Decrypt a file
        Returns: (output_file_path, metadata)
        """
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        print(f"📄 Decrypting: {input_path.name}")
        
        # Read encrypted file
        with open(input_path, 'r') as f:
            encrypted_data = json.load(f)
        
        # Default output file
        if output_file is None:
            original_name = encrypted_data.get('original_filename', 'decrypted_file')
            output_file = str(input_path.parent / f"decrypted_{original_name}")
        
        # Decrypt
        print(f"   🔓 Decrypting with {encrypted_data['algorithm']}...")
        start_time = time.time()
        decrypted_data = self.engine.decrypt_data(encrypted_data, self.keys)
        decrypt_time = (time.time() - start_time) * 1000
        
        # Save decrypted file
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
        
        print(f"   ✅ Decrypted in {decrypt_time:.2f}ms")
        print(f"   💾 Output: {output_file}")
        print(f"   📊 Size: {len(decrypted_data):,} bytes")
        
        return output_file, decrypted_data
    
    def encrypt_directory(self, input_dir, output_dir=None):
        """Encrypt all files in a directory"""
        input_path = Path(input_dir)
        
        if output_dir is None:
            output_dir = input_path.parent / f"{input_path.name}_encrypted"
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Get all files
        files = [f for f in input_path.rglob('*') if f.is_file()]
        
        print(f"\n📁 Encrypting directory: {input_dir}")
        print(f"   Files found: {len(files)}")
        print(f"   Output: {output_dir}\n")
        
        results = []
        for i, file in enumerate(files, 1):
            print(f"[{i}/{len(files)}]")
            relative_path = file.relative_to(input_path)
            output_file = output_path / f"{relative_path}.encrypted"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                encrypted_file, metadata = self.encrypt_file(file, output_file)
                results.append({'file': str(file), 'status': 'success', 'output': encrypted_file})
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results.append({'file': str(file), 'status': 'error', 'error': str(e)})
            print()
        
        # Summary
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"\n{'='*70}")
        print(f"ENCRYPTION SUMMARY")
        print(f"{'='*70}")
        print(f"Total files: {len(files)}")
        print(f"Successful: {success_count}")
        print(f"Failed: {len(files) - success_count}")
        print(f"{'='*70}")
        
        return results

def demo():
    """Demonstrate file encryption"""
    print("="*70)
    print("FILE ENCRYPTION DEMO")
    print("="*70)
    
    # Create test directory structure
    test_dir = Path('../data/test_files')
    test_dir.mkdir(parents=True, exist_ok=True)
    
    keys_dir = Path('../data/keys')
    keys_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample files
    print("\n📝 Creating sample files...")
    sample_files = [
        ('document.txt', 'This is a confidential document with sensitive information.'),
        ('data.json', '{"secret": "quantum-safe encryption", "level": "top-secret"}'),
        ('report.md', '# Secret Report\n\nThis report contains classified information.'),
    ]
    
    for filename, content in sample_files:
        file_path = test_dir / filename
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"   ✅ Created: {filename} ({len(content)} bytes)")
    
    # Test each algorithm
    for algorithm in ['kyber768', 'rsa2048', 'hybrid']:
        print(f"\n{'='*70}")
        print(f"TESTING: {algorithm.upper()}")
        print(f"{'='*70}")
        
        # Initialize encryptor
        encryptor = FileEncryptor(algorithm)
        
        # Generate and save keys
        print(f"\n🔑 Generating {algorithm} keys...")
        algo_keys_dir = keys_dir / algorithm
        algo_keys_dir.mkdir(exist_ok=True)
        encryptor.generate_keys(save_to=algo_keys_dir)
        
        # Encrypt files
        print(f"\n🔒 Encrypting files...")
        test_file = test_dir / 'document.txt'
        output_file = test_dir / f'document_{algorithm}.encrypted'
        
        encryptor.encrypt_file(test_file, output_file)
        
        # Decrypt file
        print(f"\n🔓 Decrypting file...")
        decrypted_file = test_dir / f'document_{algorithm}_decrypted.txt'
        encryptor.decrypt_file(output_file, decrypted_file)
        
        # Verify
        with open(test_file, 'r') as f:
            original = f.read()
        with open(decrypted_file, 'r') as f:
            decrypted = f.read()
        
        if original == decrypted:
            print(f"   ✅ Verification PASSED!")
        else:
            print(f"   ❌ Verification FAILED!")
    
    print("\n" + "="*70)
    print("DEMO COMPLETED")
    print("="*70)
    print(f"\nTest files created in: {test_dir}")
    print(f"Keys saved in: {keys_dir}")

if __name__ == "__main__":
    demo()
