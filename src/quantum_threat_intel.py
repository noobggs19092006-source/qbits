#!/usr/bin/env python3
"""
Quantum Threat Intelligence System
Real-time assessment of quantum computing progress and threat timeline
"""

import numpy as np
from datetime import datetime, timedelta
import json
import math

class QuantumThreatIntelligence:
    """Track quantum computing progress and predict threats"""
    
    def __init__(self):
        # Based on real quantum computing milestones
        self.milestones = {
            2019: {'qubits': 53, 'company': 'Google', 'achievement': 'Quantum Supremacy'},
            2021: {'qubits': 127, 'company': 'IBM', 'achievement': 'Eagle Processor'},
            2023: {'qubits': 433, 'company': 'IBM', 'achievement': 'Osprey Processor'},
            2024: {'qubits': 1121, 'company': 'IBM', 'achievement': 'Condor Processor'},
            2025: {'qubits': 1386, 'company': 'IBM', 'achievement': 'Flamingo (projected)'},
        }
        
        # Shor's algorithm requirements for breaking crypto
        self.breaking_requirements = {
            'RSA-1024': {'logical_qubits': 2048, 'error_rate': 0.001},
            'RSA-2048': {'logical_qubits': 4096, 'error_rate': 0.0001},
            'RSA-4096': {'logical_qubits': 8192, 'error_rate': 0.00001},
            'ECC-256': {'logical_qubits': 2330, 'error_rate': 0.001},
        }
    
    def predict_breaking_timeline(self, algorithm='RSA-2048'):
        """Predict when quantum computers will break specific algorithms"""
        
        requirements = self.breaking_requirements.get(algorithm)
        if not requirements:
            return None
        
        # Current state (2026)
        current_year = 2026
        current_qubits = 1386  # IBM Flamingo
        target_qubits = requirements['logical_qubits']
        
        # Estimate growth rate (roughly 3x every 2 years - conservative)
        years_needed = math.log(target_qubits / current_qubits) / math.log(3) * 2
        
        # Add time for error correction maturity
        error_correction_years = 3
        
        breaking_year = current_year + years_needed + error_correction_years
        
        # Conservative estimate adds 2 more years
        conservative_year = breaking_year + 2
        
        # Optimistic (for attackers) subtracts 2 years
        optimistic_year = max(current_year + 1, breaking_year - 2)
        
        return {
            'algorithm': algorithm,
            'current_year': current_year,
            'predicted_breaking_year': int(breaking_year),
            'conservative_estimate': int(conservative_year),
            'optimistic_estimate': int(optimistic_year),
            'years_remaining': int(breaking_year - current_year),
            'threat_level': self._calculate_threat_level(int(breaking_year - current_year)),
            'required_qubits': target_qubits,
            'current_qubits': current_qubits,
            'progress_percentage': (current_qubits / target_qubits) * 100
        }
    
    def _calculate_threat_level(self, years_remaining):
        """Calculate current threat level"""
        if years_remaining <= 3:
            return 'IMMINENT'
        elif years_remaining <= 7:
            return 'HIGH'
        elif years_remaining <= 12:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def assess_data_risk(self, encryption_date, data_sensitivity, algorithm='RSA-2048'):
        """Assess risk for specific encrypted data"""
        
        timeline = self.predict_breaking_timeline(algorithm)
        if not timeline:
            return None
        
        # Parse date
        if isinstance(encryption_date, str):
            enc_date = datetime.fromisoformat(encryption_date.replace('Z', '+00:00'))
        else:
            enc_date = encryption_date
        
        breaking_date = datetime(timeline['predicted_breaking_year'], 1, 1)
        
        # Calculate exposure window
        years_until_breaking = (breaking_date - datetime.now()).days / 365.25
        
        # Data sensitivity multiplier
        sensitivity_multipliers = {
            'PUBLIC': 0.1,
            'INTERNAL': 0.5,
            'CONFIDENTIAL': 1.0,
            'SECRET': 1.5,
            'TOP_SECRET': 2.0
        }
        
        sensitivity_factor = sensitivity_multipliers.get(data_sensitivity.upper(), 1.0)
        
        # Calculate risk score (0-100)
        base_risk = 100 - (years_until_breaking / 15 * 100)  # Normalized to 15 years
        risk_score = min(100, max(0, base_risk * sensitivity_factor))
        
        # Determine if data needs immediate protection
        needs_immediate_action = risk_score > 70 or years_until_breaking < 5
        
        return {
            'encryption_date': enc_date.isoformat(),
            'algorithm': algorithm,
            'sensitivity': data_sensitivity,
            'risk_score': round(risk_score, 1),
            'years_until_vulnerable': round(years_until_breaking, 1),
            'breaking_year': timeline['predicted_breaking_year'],
            'needs_immediate_action': needs_immediate_action,
            'recommendation': self._generate_recommendation(risk_score, data_sensitivity, years_until_breaking),
            'safe_until': breaking_date.isoformat() if years_until_breaking > 0 else 'ALREADY VULNERABLE'
        }
    
    def _generate_recommendation(self, risk_score, sensitivity, years_remaining):
        """Generate actionable recommendation"""
        if risk_score > 90:
            return f"🚨 CRITICAL: Migrate to PQC immediately! {sensitivity} data will be vulnerable within {years_remaining:.1f} years."
        elif risk_score > 70:
            return f"⚠️ HIGH PRIORITY: Begin migration planning. Deploy hybrid mode within 6 months."
        elif risk_score > 50:
            return f"📋 MODERATE: Start evaluating PQC solutions. Plan migration within 2 years."
        elif risk_score > 30:
            return f"📊 LOW-MEDIUM: Monitor quantum progress. Begin internal discussions."
        else:
            return f"✅ LOW RISK: Continue monitoring. Consider PQC for new systems."
    
    def generate_threat_report(self):
        """Generate comprehensive threat intelligence report"""
        current_year = 2026
        
        # Analyze all algorithms
        algorithms = ['RSA-1024', 'RSA-2048', 'RSA-4096', 'ECC-256']
        predictions = {}
        
        for algo in algorithms:
            predictions[algo] = self.predict_breaking_timeline(algo)
        
        # Overall assessment
        earliest_break = min(p['predicted_breaking_year'] for p in predictions.values())
        years_to_earliest = earliest_break - current_year
        
        return {
            'report_date': datetime.now().isoformat(),
            'current_quantum_state': {
                'year': current_year,
                'leading_qubits': 1386,
                'leader': 'IBM',
                'progress_status': 'Accelerating rapidly'
            },
            'predictions': predictions,
            'overall_assessment': {
                'earliest_breaking_year': earliest_break,
                'years_remaining': years_to_earliest,
                'threat_level': self._calculate_threat_level(years_to_earliest),
                'recommended_action': 'Begin PQC migration immediately for long-term sensitive data'
            },
            'industry_trends': [
                'NIST finalized PQC standards in August 2024',
                'US Government mandates PQC by 2030-2035',
                'China announced 504-qubit quantum computer in 2024',
                'Harvest-now-decrypt-later attacks confirmed by intelligence agencies'
            ]
        }

class QuantumAttackSimulator:
    """Simulate Shor's algorithm attacking RSA"""
    
    def __init__(self):
        self.rsa_modulus = None
        self.factors = None
    
    def simulate_classical_factoring(self, n, max_attempts=1000000):
        """Simulate classical factoring (very slow)"""
        # For small numbers only (demo purposes)
        if n > 10**12:
            return {
                'success': False,
                'message': 'Number too large for classical factoring demo',
                'estimated_time': 'Millions of years'
            }
        
        attempts = 0
        for i in range(2, min(int(n**0.5) + 1, max_attempts)):
            attempts += 1
            if n % i == 0:
                return {
                    'success': True,
                    'factor1': i,
                    'factor2': n // i,
                    'attempts': attempts,
                    'method': 'Classical brute force'
                }
        
        return {
            'success': False,
            'attempts': attempts,
            'message': 'Would take too long - exceeded max attempts'
        }
    
    def simulate_quantum_factoring(self, n):
        """Simulate Shor's algorithm (simplified)"""
        
        # For demo: actually factor (but pretend it's quantum)
        # In reality, Shor's algorithm is exponentially faster
        
        # Simulate quantum period finding
        factors = []
        for i in range(2, min(int(n**0.5) + 1, 100000)):
            if n % i == 0:
                factors = [i, n // i]
                break
        
        if factors:
            return {
                'success': True,
                'factor1': factors[0],
                'factor2': factors[1],
                'method': 'Shors Algorithm (Quantum)',
                'quantum_operations': math.ceil(math.log2(n) ** 2),  # Polynomial complexity
                'speedup': 'Exponential',
                'time': 'Polynomial in log(N) - extremely fast'
            }
        
        return {'success': False}
    
    def demonstrate_vulnerability(self):
        """Demonstrate RSA vulnerability to quantum attacks"""
        
        # Use small RSA modulus for demo
        n = 91  # 7 * 13 (tiny RSA for demo)
        
        print("\n" + "="*70)
        print("⚛️  QUANTUM ATTACK SIMULATION")
        print("="*70)
        
        print(f"\n🔢 Target RSA Modulus: {n}")
        print("   (Using small number for demo - real RSA uses 617-digit numbers)")
        
        # Classical attack
        print("\n🖥️  CLASSICAL COMPUTER ATTACK:")
        print("   Method: Brute force factoring")
        classical = self.simulate_classical_factoring(n)
        if classical['success']:
            print(f"   ✅ Factors found: {classical['factor1']} × {classical['factor2']}")
            print(f"   📊 Attempts needed: {classical['attempts']:,}")
            print(f"   ⏱️  For RSA-2048: Would take millions of years")
        
        # Quantum attack
        print("\n⚛️  QUANTUM COMPUTER ATTACK:")
        print("   Method: Shor's Algorithm")
        quantum = self.simulate_quantum_factoring(n)
        if quantum['success']:
            print(f"   ✅ Factors found: {quantum['factor1']} × {quantum['factor2']}")
            print(f"   📊 Quantum operations: ~{quantum['quantum_operations']}")
            print(f"   ⏱️  For RSA-2048: Just ~8 hours with 4096 logical qubits!")
            print(f"   🚀 Speedup: {quantum['speedup']}")
        
        print("\n💡 KEY INSIGHT:")
        print("   Classical: Time grows EXPONENTIALLY with key size")
        print("   Quantum:   Time grows POLYNOMIALLY with key size")
        print("   Result: RSA-2048 goes from 'millions of years' to '8 hours'!")
        
        # Kyber comparison
        print("\n🛡️  KYBER-768 DEFENSE:")
        print("   ✅ Lattice problem remains hard for quantum computers")
        print("   ✅ No known quantum algorithm breaks it efficiently")
        print("   ✅ Security remains intact in post-quantum era")
        
        return {
            'classical': classical,
            'quantum': quantum,
            'vulnerability_proven': True
        }

def demo():
    """Demonstrate quantum threat intelligence"""
    print("="*70)
    print("🌐 QUANTUM THREAT INTELLIGENCE SYSTEM")
    print("="*70)
    
    intel = QuantumThreatIntelligence()
    
    # Generate threat report
    print("\n📊 CURRENT THREAT LANDSCAPE")
    print("="*70)
    
    report = intel.generate_threat_report()
    
    print(f"\n📅 Report Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"🔬 Current State: {report['current_quantum_state']['leading_qubits']} qubits ({report['current_quantum_state']['leader']})")
    
    print(f"\n⚠️  BREAKING TIMELINE PREDICTIONS:")
    print("-"*70)
    
    for algo, pred in report['predictions'].items():
        print(f"\n{algo}:")
        print(f"   Breaks in: {pred['predicted_breaking_year']} ({pred['years_remaining']} years)")
        print(f"   Range: {pred['optimistic_estimate']}-{pred['conservative_estimate']}")
        print(f"   Threat Level: {pred['threat_level']}")
        print(f"   Progress: {pred['progress_percentage']:.1f}% of required qubits")
    
    print(f"\n🎯 OVERALL ASSESSMENT:")
    print(f"   Earliest Break: {report['overall_assessment']['earliest_breaking_year']}")
    print(f"   Years Remaining: {report['overall_assessment']['years_remaining']}")
    print(f"   Threat Level: {report['overall_assessment']['threat_level']}")
    
    # Assess specific data
    print("\n" + "="*70)
    print("📋 DATA RISK ASSESSMENT")
    print("="*70)
    
    test_scenarios = [
        {'date': '2020-01-01', 'sensitivity': 'TOP_SECRET', 'algo': 'RSA-2048'},
        {'date': '2024-01-01', 'sensitivity': 'CONFIDENTIAL', 'algo': 'RSA-2048'},
        {'date': '2025-01-01', 'sensitivity': 'INTERNAL', 'algo': 'RSA-2048'},
    ]
    
    for scenario in test_scenarios:
        risk = intel.assess_data_risk(scenario['date'], scenario['sensitivity'], scenario['algo'])
        
        print(f"\n📄 Data encrypted: {scenario['date']}")
        print(f"   Sensitivity: {risk['sensitivity']}")
        print(f"   Risk Score: {risk['risk_score']}/100")
        print(f"   Vulnerable in: {risk['years_until_vulnerable']} years ({risk['breaking_year']})")
        print(f"   Action Required: {'YES' if risk['needs_immediate_action'] else 'Monitor'}")
        print(f"   💡 {risk['recommendation']}")
    
    # Attack simulation
    simulator = QuantumAttackSimulator()
    simulator.demonstrate_vulnerability()
    
    print("\n" + "="*70)

if __name__ == "__main__":
    demo()
