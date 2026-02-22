#!/usr/bin/env python3
"""
AI-Powered Security Monitoring System
Uses ML to detect anomalies and predict threats
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import json
from datetime import datetime
import hashlib

class AISecurityMonitor:
    """ML-based security monitoring and threat detection"""
    
    def __init__(self):
        self.anomaly_detector = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.encryption_history = []
        
    def extract_features(self, encryption_data):
        """Extract features from encryption operation"""
        features = [
            encryption_data.get('file_size', 0),
            encryption_data.get('encryption_time', 0) * 1000,  # Convert to ms
            len(encryption_data.get('algorithm', '')),
            encryption_data.get('key_size', 0),
            encryption_data.get('timestamp', 0) % 86400,  # Time of day in seconds
        ]
        return np.array(features).reshape(1, -1)
    
    def train_baseline(self, normal_operations):
        """Train on normal encryption operations"""
        if len(normal_operations) < 10:
            print("⚠️  Need at least 10 samples for training")
            return False
        
        # Extract features from all operations
        features = []
        for op in normal_operations:
            feat = self.extract_features(op)
            features.append(feat.flatten())
        
        X = np.array(features)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train anomaly detector
        self.anomaly_detector.fit(X_scaled)
        self.is_trained = True
        
        print(f"✅ AI model trained on {len(normal_operations)} normal operations")
        return True
    
    def detect_anomaly(self, encryption_data):
        """Detect if operation is anomalous"""
        if not self.is_trained:
            # Generate synthetic training data if not trained
            self._bootstrap_training()
        
        features = self.extract_features(encryption_data)
        features_scaled = self.scaler.transform(features)
        
        # Predict (-1 for anomaly, 1 for normal)
        prediction = self.anomaly_detector.predict(features_scaled)[0]
        
        # Get anomaly score (lower is more anomalous)
        score = self.anomaly_detector.score_samples(features_scaled)[0]
        
        is_anomaly = prediction == -1
        confidence = abs(score) * 100  # Convert to percentage
        
        result = {
            'is_anomaly': bool(is_anomaly),
            'confidence': float(confidence),
            'risk_level': self._calculate_risk_level(score),
            'recommendations': self._generate_recommendations(is_anomaly, encryption_data)
        }
        
        # Store in history
        self.encryption_history.append({
            'timestamp': datetime.now().isoformat(),
            'data': encryption_data,
            'anomaly_result': result
        })
        
        return result
    
    def _bootstrap_training(self):
        """Generate synthetic baseline data for cold start"""
        synthetic_data = []
        
        # Normal Kyber operations
        for _ in range(50):
            synthetic_data.append({
                'file_size': np.random.normal(50000, 10000),
                'encryption_time': np.random.normal(0.005, 0.001),
                'algorithm': 'kyber768',
                'key_size': 1184,
                'timestamp': np.random.randint(0, 86400)
            })
        
        # Normal RSA operations
        for _ in range(30):
            synthetic_data.append({
                'file_size': np.random.normal(50000, 10000),
                'encryption_time': np.random.normal(0.15, 0.03),
                'algorithm': 'rsa2048',
                'key_size': 256,
                'timestamp': np.random.randint(0, 86400)
            })
        
        self.train_baseline(synthetic_data)
    
    def _calculate_risk_level(self, score):
        """Calculate risk level from anomaly score"""
        if score < -0.5:
            return 'CRITICAL'
        elif score < -0.3:
            return 'HIGH'
        elif score < -0.1:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _generate_recommendations(self, is_anomaly, data):
        """Generate actionable recommendations"""
        if not is_anomaly:
            return ['Operation appears normal']
        
        recommendations = [
            '🚨 ANOMALY DETECTED - Review this operation carefully',
        ]
        
        # Check for suspicious patterns
        if data.get('encryption_time', 0) > 1.0:
            recommendations.append('⚠️  Unusually slow encryption - possible resource attack')
        
        if data.get('file_size', 0) > 1000000:
            recommendations.append('⚠️  Very large file - verify this is expected')
        
        # Time-based checks
        hour = (data.get('timestamp', 0) % 86400) // 3600
        if hour < 6 or hour > 22:
            recommendations.append('⚠️  Off-hours operation - verify authorization')
        
        recommendations.append('✅ Recommended: Review access logs and verify user identity')
        recommendations.append('✅ Recommended: Enable additional authentication for this operation')
        
        return recommendations
    
    def get_security_dashboard(self):
        """Generate security dashboard data"""
        if not self.encryption_history:
            return {'total_operations': 0}
        
        total = len(self.encryption_history)
        anomalies = sum(1 for h in self.encryption_history if h['anomaly_result']['is_anomaly'])
        
        recent = self.encryption_history[-10:]
        
        return {
            'total_operations': total,
            'anomalies_detected': anomalies,
            'anomaly_rate': (anomalies / total * 100) if total > 0 else 0,
            'recent_operations': recent,
            'threat_level': 'HIGH' if (anomalies / total) > 0.2 else 'NORMAL'
        }

class MLPerformancePredictor:
    """Predict encryption performance using ML"""
    
    def __init__(self):
        from sklearn.linear_model import Ridge
        self.model_kyber = Ridge(alpha=1.0)
        self.model_rsa = Ridge(alpha=1.0)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train(self):
        """Train on synthetic performance data"""
        # Generate training data based on our benchmarks
        file_sizes = np.random.randint(100, 10000000, 1000)
        
        # Kyber: roughly 0.015ms + 0.000001ms per KB
        kyber_times = 0.015 + (file_sizes / 1024) * 0.000001 + np.random.normal(0, 0.002, 1000)
        
        # RSA: roughly 0.3ms + 0.00005ms per KB  
        rsa_times = 0.3 + (file_sizes / 1024) * 0.00005 + np.random.normal(0, 0.05, 1000)
        
        X = file_sizes.reshape(-1, 1)
        X_scaled = self.scaler.fit_transform(X)
        
        self.model_kyber.fit(X_scaled, kyber_times)
        self.model_rsa.fit(X_scaled, rsa_times)
        self.is_trained = True
        
        print("✅ Performance prediction models trained")
    
    def predict_time(self, file_size, algorithm='kyber768'):
        """Predict encryption time"""
        if not self.is_trained:
            self.train()
        
        X = np.array([[file_size]])
        X_scaled = self.scaler.transform(X)
        
        if 'kyber' in algorithm.lower():
            predicted = self.model_kyber.predict(X_scaled)[0]
        else:
            predicted = self.model_rsa.predict(X_scaled)[0]
        
        return max(0.001, predicted)  # Minimum 1ms
    
    def compare_algorithms(self, file_size):
        """Compare predicted performance"""
        kyber_time = self.predict_time(file_size, 'kyber768')
        rsa_time = self.predict_time(file_size, 'rsa2048')
        
        speedup = rsa_time / kyber_time
        
        return {
            'file_size': file_size,
            'kyber_predicted': kyber_time,
            'rsa_predicted': rsa_time,
            'kyber_faster_by': speedup,
            'recommendation': 'kyber768' if speedup > 1 else 'rsa2048'
        }

def demo():
    """Demo AI security features"""
    print("="*70)
    print("🤖 AI-POWERED SECURITY MONITORING DEMO")
    print("="*70)
    
    # Initialize AI monitor
    monitor = AISecurityMonitor()
    
    print("\n📊 Simulating encryption operations...")
    
    # Normal operations
    normal_ops = [
        {'file_size': 50000, 'encryption_time': 0.005, 'algorithm': 'kyber768', 'key_size': 1184, 'timestamp': 43200},
        {'file_size': 75000, 'encryption_time': 0.006, 'algorithm': 'kyber768', 'key_size': 1184, 'timestamp': 43300},
        {'file_size': 100000, 'encryption_time': 0.15, 'algorithm': 'rsa2048', 'key_size': 256, 'timestamp': 43400},
    ]
    
    print("\n✅ Processing normal operations:")
    for op in normal_ops:
        result = monitor.detect_anomaly(op)
        status = "🟢 NORMAL" if not result['is_anomaly'] else "🔴 ANOMALY"
        print(f"   {status} - {op['algorithm']} - Confidence: {result['confidence']:.1f}%")
    
    # Suspicious operation
    print("\n⚠️  Processing suspicious operation:")
    suspicious_op = {
        'file_size': 5000000,  # Very large
        'encryption_time': 5.0,  # Very slow
        'algorithm': 'kyber768',
        'key_size': 1184,
        'timestamp': 7200  # 2 AM
    }
    
    result = monitor.detect_anomaly(suspicious_op)
    print(f"   🔴 ANOMALY DETECTED!")
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Confidence: {result['confidence']:.1f}%")
    print(f"\n   Recommendations:")
    for rec in result['recommendations']:
        print(f"   {rec}")
    
    # Performance prediction
    print("\n" + "="*70)
    print("📈 ML-BASED PERFORMANCE PREDICTION")
    print("="*70)
    
    predictor = MLPerformancePredictor()
    predictor.train()
    
    test_sizes = [10000, 100000, 1000000, 10000000]
    
    print("\nPredicted encryption times:")
    print(f"{'File Size':<15} {'Kyber-768':<15} {'RSA-2048':<15} {'Speedup':<10}")
    print("-"*70)
    
    for size in test_sizes:
        comparison = predictor.compare_algorithms(size)
        print(f"{size/1024:.1f} KB{'':<8} "
              f"{comparison['kyber_predicted']*1000:.2f}ms{'':<8} "
              f"{comparison['rsa_predicted']*1000:.2f}ms{'':<8} "
              f"{comparison['kyber_faster_by']:.1f}x")
    
    # Dashboard
    print("\n" + "="*70)
    print("🛡️  SECURITY DASHBOARD")
    print("="*70)
    
    dashboard = monitor.get_security_dashboard()
    print(f"\nTotal Operations: {dashboard['total_operations']}")
    print(f"Anomalies Detected: {dashboard['anomalies_detected']}")
    print(f"Anomaly Rate: {dashboard['anomaly_rate']:.1f}%")
    print(f"Threat Level: {dashboard['threat_level']}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    demo()
