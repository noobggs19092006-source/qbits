#!/usr/bin/env python3
"""
Live Quantum Attack Visualization
Shows RSA being broken vs Kyber surviving
"""

import random
import time

class QuantumAttackSimulator:
    """Simulates quantum attack on different algorithms"""
    
    def simulate_attack(self, algorithm, key_size):
        """Simulate a quantum attack"""
        
        if algorithm.lower() == 'rsa':
            return self._simulate_rsa_attack(key_size)
        elif algorithm.lower() == 'kyber':
            return self._simulate_kyber_attack(key_size)
    
    def _simulate_rsa_attack(self, key_size):
        """Simulate Shor's algorithm breaking RSA"""
        stages = []
        
        # Stage 1: Setup
        stages.append({
            'stage': 'initialization',
            'progress': 10,
            'message': 'Quantum computer initialized with 4096 qubits',
            'time': 0.1,
            'vulnerable': True
        })
        
        # Stage 2: Period finding
        stages.append({
            'stage': 'period_finding',
            'progress': 35,
            'message': 'Running Quantum Fourier Transform for period finding',
            'time': 0.5,
            'vulnerable': True
        })
        
        # Stage 3: Classical computation
        stages.append({
            'stage': 'classical_processing',
            'progress': 65,
            'message': 'Computing factors using quantum results',
            'time': 0.3,
            'vulnerable': True
        })
        
        # Stage 4: BROKEN
        stages.append({
            'stage': 'factorization_complete',
            'progress': 100,
            'message': f'🚨 RSA-{key_size} BROKEN! Factors found in 8.3 hours',
            'time': 0.2,
            'vulnerable': True,
            'broken': True,
            'factors': 'p = [REDACTED], q = [REDACTED]'
        })
        
        return stages
    
    def _simulate_kyber_attack(self, key_size):
        """Simulate quantum attack failing on Kyber"""
        stages = []
        
        # Stage 1: Setup
        stages.append({
            'stage': 'initialization',
            'progress': 10,
            'message': 'Quantum computer initialized with 4096 qubits',
            'time': 0.1,
            'vulnerable': False
        })
        
        # Stage 2: Lattice analysis
        stages.append({
            'stage': 'lattice_analysis',
            'progress': 30,
            'message': 'Attempting to solve Shortest Vector Problem in 256-dimensional lattice',
            'time': 0.5,
            'vulnerable': False
        })
        
        # Stage 3: Grover's algorithm
        stages.append({
            'stage': 'grovers_attempt',
            'progress': 50,
            'message': 'Grover\'s algorithm reduces security by half (still 96-bit quantum security)',
            'time': 0.4,
            'vulnerable': False
        })
        
        # Stage 4: Failure
        stages.append({
            'stage': 'attack_failed',
            'progress': 75,
            'message': 'No efficient quantum algorithm for lattice problems exists',
            'time': 0.3,
            'vulnerable': False
        })
        
        # Stage 5: SECURE
        stages.append({
            'stage': 'kyber_secure',
            'progress': 100,
            'message': f'✅ Kyber-{key_size} REMAINS SECURE! Attack failed after 10,000+ years equivalent',
            'time': 0.2,
            'vulnerable': False,
            'broken': False
        })
        
        return stages

def demo():
    simulator = QuantumAttackSimulator()
    
    print("="*70)
    print("⚛️  QUANTUM ATTACK SIMULATION")
    print("="*70)
    
    print("\n🔴 ATTACKING RSA-2048...")
    print("-"*70)
    rsa_stages = simulator.simulate_attack('rsa', 2048)
    for stage in rsa_stages:
        time.sleep(stage['time'])
        print(f"[{stage['progress']}%] {stage['message']}")
    
    print("\n\n🟢 ATTACKING KYBER-768...")
    print("-"*70)
    kyber_stages = simulator.simulate_attack('kyber', 768)
    for stage in kyber_stages:
        time.sleep(stage['time'])
        print(f"[{stage['progress']}%] {stage['message']}")
    
    print("\n" + "="*70)
    print("VERDICT: Kyber-768 withstands quantum attacks!")
    print("="*70)

if __name__ == "__main__":
    demo()
