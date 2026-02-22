#!/usr/bin/env python3
"""
Enterprise Migration Toolkit
Assesses cryptographic systems and provides migration roadmap
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime, timedelta
import hashlib

class MigrationAssessment:
    """Assess current cryptographic infrastructure"""
    
    # Known vulnerable patterns
    VULNERABLE_PATTERNS = {
        'RSA': [
            r'RSA\.generate\(\d+\)',
            r'from Crypto\.PublicKey import RSA',
            r'openssl rsa',
            r'ssh-rsa',
        ],
        'ECC': [
            r'ECC\.generate',
            r'ecdsa',
            r'secp256k1',
        ],
        'DH': [
            r'DiffieHellman',
            r'DHParameters',
        ]
    }
    
    def __init__(self):
        self.findings = []
        self.risk_score = 0
        
    def scan_directory(self, directory):
        """Scan directory for vulnerable crypto usage"""
        print(f"🔍 Scanning directory: {directory}")
        print("="*70)
        
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"❌ Directory not found: {directory}")
            return
        
        # Get all relevant files
        extensions = ['.py', '.java', '.js', '.cpp', '.c', '.h', '.go', '.rs', '.sh']
        files = []
        for ext in extensions:
            files.extend(dir_path.rglob(f'*{ext}'))
        
        print(f"📁 Found {len(files)} files to scan\n")
        
        vulnerable_files = []
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                file_findings = self._scan_content(content, str(file_path))
                if file_findings:
                    vulnerable_files.append({
                        'file': str(file_path),
                        'findings': file_findings
                    })
                    self.findings.extend(file_findings)
                    
            except Exception as e:
                pass
        
        return vulnerable_files
    
    def _scan_content(self, content, filename):
        """Scan file content for vulnerable patterns"""
        findings = []
        
        for crypto_type, patterns in self.VULNERABLE_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    # Find line number
                    line_num = content[:match.start()].count('\n') + 1
                    
                    findings.append({
                        'file': filename,
                        'line': line_num,
                        'type': crypto_type,
                        'pattern': match.group(0),
                        'risk': 'HIGH' if crypto_type in ['RSA', 'ECC'] else 'MEDIUM'
                    })
                    
                    # Increase risk score
                    self.risk_score += 10 if crypto_type in ['RSA', 'ECC'] else 5
        
        return findings
    
    def generate_report(self, output_file=None):
        """Generate comprehensive migration report"""
        report = {
            'scan_date': datetime.now().isoformat(),
            'total_findings': len(self.findings),
            'risk_score': self.risk_score,
            'risk_level': self._calculate_risk_level(),
            'findings_by_type': self._group_findings(),
            'migration_timeline': self._estimate_timeline(),
            'recommendations': self._generate_recommendations(),
            'detailed_findings': self.findings[:50]  # Limit to 50 for readability
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n📄 Report saved to: {output_file}")
        
        return report
    
    def _group_findings(self):
        """Group findings by crypto type"""
        groups = {}
        for finding in self.findings:
            crypto_type = finding['type']
            if crypto_type not in groups:
                groups[crypto_type] = 0
            groups[crypto_type] += 1
        return groups
    
    def _calculate_risk_level(self):
        """Calculate overall risk level"""
        if self.risk_score >= 100:
            return 'CRITICAL'
        elif self.risk_score >= 50:
            return 'HIGH'
        elif self.risk_score >= 20:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _estimate_timeline(self):
        """Estimate migration timeline"""
        num_findings = len(self.findings)
        
        # Rough estimates
        analysis_weeks = max(1, num_findings // 20)
        testing_weeks = max(2, num_findings // 10)
        deployment_weeks = max(2, num_findings // 15)
        
        total_weeks = analysis_weeks + testing_weeks + deployment_weeks
        
        return {
            'total_weeks': total_weeks,
            'phases': {
                'Phase 1 - Analysis': f'{analysis_weeks} weeks',
                'Phase 2 - Testing': f'{testing_weeks} weeks',
                'Phase 3 - Deployment': f'{deployment_weeks} weeks'
            },
            'estimated_completion': (datetime.now() + timedelta(weeks=total_weeks)).strftime('%Y-%m-%d')
        }
    
    def _generate_recommendations(self):
        """Generate migration recommendations"""
        recommendations = [
            {
                'priority': 'IMMEDIATE',
                'action': 'Deploy Hybrid Mode',
                'description': 'Implement hybrid (RSA + Kyber) encryption for critical systems',
                'benefit': 'Provides quantum safety while maintaining backward compatibility'
            },
            {
                'priority': 'HIGH',
                'action': 'Update Key Management',
                'description': 'Upgrade key management systems to support PQC algorithms',
                'benefit': 'Enables smooth transition to quantum-safe cryptography'
            },
            {
                'priority': 'HIGH',
                'action': 'Train Development Team',
                'description': 'Educate developers on PQC best practices',
                'benefit': 'Reduces implementation errors and security gaps'
            },
            {
                'priority': 'MEDIUM',
                'action': 'Gradual Migration',
                'description': 'Replace RSA/ECC with Kyber in non-critical systems first',
                'benefit': 'Minimizes risk while gaining operational experience'
            },
            {
                'priority': 'MEDIUM',
                'action': 'Update Dependencies',
                'description': 'Ensure all libraries support NIST PQC standards',
                'benefit': 'Maintains long-term security and compliance'
            }
        ]
        
        return recommendations

    def print_summary(self):
        """Print human-readable summary"""
        print("\n" + "="*70)
        print("📊 MIGRATION ASSESSMENT SUMMARY")
        print("="*70)
        
        print(f"\n🔍 Total Findings: {len(self.findings)}")
        print(f"⚠️  Risk Score: {self.risk_score}")
        print(f"🚨 Risk Level: {self._calculate_risk_level()}")
        
        print(f"\n📈 Findings by Type:")
        for crypto_type, count in self._group_findings().items():
            print(f"   • {crypto_type}: {count}")
        
        timeline = self._estimate_timeline()
        print(f"\n⏱️  Estimated Migration Timeline: {timeline['total_weeks']} weeks")
        for phase, duration in timeline['phases'].items():
            print(f"   • {phase}: {duration}")
        
        print(f"\n🎯 Top Recommendations:")
        for rec in self._generate_recommendations()[:3]:
            print(f"\n   [{rec['priority']}] {rec['action']}")
            print(f"   → {rec['description']}")
        
        print("\n" + "="*70)

def demo():
    """Run migration assessment demo"""
    print("="*70)
    print("🔧 ENTERPRISE MIGRATION TOOLKIT DEMO")
    print("="*70)
    
    # Create sample vulnerable code
    demo_dir = Path('../data/sample_codebase')
    demo_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample vulnerable files
    sample_files = {
        'auth_service.py': '''
# Authentication Service
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class AuthService:
    def __init__(self):
        # VULNERABLE: RSA-2048 will be broken by quantum computers
        self.key = RSA.generate(2048)
        
    def encrypt_token(self, token):
        cipher = PKCS1_OAEP.new(self.key.publickey())
        return cipher.encrypt(token)
''',
        'secure_channel.py': '''
# Secure Communication Channel
from Crypto.PublicKey import ECC
import ecdsa

class SecureChannel:
    def __init__(self):
        # VULNERABLE: ECC vulnerable to quantum attacks
        self.key = ECC.generate(curve='P-256')
        
    def sign_message(self, message):
        # VULNERABLE: ECDSA signatures
        return ecdsa.sign(message, self.key)
''',
        'key_exchange.py': '''
# Key Exchange Protocol
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_key_pair():
    # VULNERABLE: RSA key exchange
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key
'''
    }
    
    print(f"\n📝 Creating sample codebase with vulnerable crypto...")
    for filename, content in sample_files.items():
        file_path = demo_dir / filename
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"   ✅ Created: {filename}")
    
    # Run assessment
    print(f"\n{'='*70}")
    assessor = MigrationAssessment()
    vulnerable_files = assessor.scan_directory(demo_dir)
    
    # Print findings
    if vulnerable_files:
        print(f"\n⚠️  VULNERABLE FILES DETECTED:")
        print("="*70)
        for vf in vulnerable_files:
            print(f"\n📄 {Path(vf['file']).name}")
            for finding in vf['findings']:
                print(f"   Line {finding['line']}: {finding['type']} - {finding['pattern']}")
                print(f"   Risk: {finding['risk']}")
    
    # Generate report
    report_path = '../data/migration_report.json'
    report = assessor.generate_report(report_path)
    
    # Print summary
    assessor.print_summary()
    
    print(f"\n💡 NEXT STEPS:")
    print("   1. Review the detailed report in: {report_path}")
    print("   2. Prioritize critical systems for immediate hybrid mode deployment")
    print("   3. Begin phased migration according to the timeline")
    print("   4. Monitor and test throughout the transition period")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    demo()
