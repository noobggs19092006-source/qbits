#!/usr/bin/env python3
"""
AI-Powered Cryptography Assistant
Natural language interface for crypto questions
"""

import re
from datetime import datetime

class CryptoAssistant:
    """AI assistant that answers crypto questions in plain English"""
    
    def __init__(self):
        self.knowledge_base = self._build_knowledge_base()
        self.conversation_history = []
        
    def _build_knowledge_base(self):
        """Build comprehensive knowledge base"""
        return {
            'kyber': {
                'keywords': ['kyber', 'lattice', 'crystals', 'pqc', 'post-quantum'],
                'info': """Kyber-768 is a post-quantum encryption algorithm approved by NIST in 2024. 
It uses lattice-based mathematics that quantum computers cannot break efficiently. 
It provides 192-bit security and is 6,515x faster than RSA at key generation."""
            },
            'rsa': {
                'keywords': ['rsa', 'factoring', 'public key', 'rivest shamir'],
                'info': """RSA is the current standard for public-key encryption, invented in 1977. 
It relies on the difficulty of factoring large numbers. However, quantum computers running 
Shor's algorithm can break RSA in polynomial time (about 8 hours for RSA-2048 with 4096 qubits)."""
            },
            'quantum_threat': {
                'keywords': ['quantum', 'threat', 'shor', 'harvest', 'break', 'vulnerable'],
                'info': """The quantum threat is real and approaching. By 2029-2030, quantum computers 
will be powerful enough to break RSA-2048. The "harvest now, decrypt later" attack means 
adversaries are storing encrypted data today to decrypt when quantum computers are available. 
Any data encrypted with RSA today that needs protection beyond 2030 is at risk."""
            },
            'hybrid': {
                'keywords': ['hybrid', 'transition', 'both', 'combined'],
                'info': """Hybrid encryption uses both classical (RSA) and post-quantum (Kyber) 
algorithms together. This provides security against both classical and quantum attacks during 
the transition period. If either algorithm is broken, the other still protects your data."""
            },
            'migration': {
                'keywords': ['migrate', 'transition', 'upgrade', 'switch', 'move'],
                'info': """Migration to PQC should follow a 3-phase approach:
1. Assessment: Scan systems for vulnerable cryptography (1-2 weeks)
2. Hybrid Deployment: Implement hybrid mode for critical systems (2-4 months)
3. Full Migration: Complete transition to PQC (6-18 months)
Start with high-value, long-term sensitive data first."""
            },
            'timeline': {
                'keywords': ['when', 'timeline', 'how long', 'date', 'year'],
                'info': """Key timeline milestones:
- 2024: NIST standardized PQC algorithms
- 2026: Current year - hybrid mode recommended
- 2029: RSA-1024 and ECC-256 likely broken
- 2030: RSA-2048 likely broken
- 2030-2035: US Government PQC mandate
Start planning NOW for any data that needs protection beyond 2030."""
            },
            'performance': {
                'keywords': ['fast', 'slow', 'speed', 'performance', 'time'],
                'info': """Kyber-768 is actually FASTER than RSA-2048:
- Key Generation: 6,515x faster
- Encryption: 21x faster  
- Decryption: 67x faster
The only tradeoff is slightly larger key sizes (1184 bytes vs 450 bytes), but this is 
negligible for modern systems."""
            },
            'nist': {
                'keywords': ['nist', 'standard', 'approved', 'official'],
                'info': """NIST (National Institute of Standards and Technology) ran a 6-year 
competition evaluating 69 algorithms from around the world. In August 2024, they standardized:
- ML-KEM (Kyber) for encryption
- ML-DSA (Dilithium) for digital signatures
- SLH-DSA (SPHINCS+) for hash-based signatures
These are now the official standards for post-quantum cryptography."""
            }
        }
    
    def answer_question(self, question):
        """Process question and generate answer"""
        question_lower = question.lower()
        
        # Store in history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'type': 'user'
        })
        
        # Check for specific patterns
        if 'how' in question_lower and ('work' in question_lower or 'works' in question_lower):
            return self._explain_how_it_works(question_lower)
        
        if 'why' in question_lower:
            return self._explain_why(question_lower)
        
        if 'what' in question_lower and ('is' in question_lower or 'are' in question_lower):
            return self._explain_what(question_lower)
        
        if any(word in question_lower for word in ['should', 'recommend', 'advice']):
            return self._give_recommendation(question_lower)
        
        if any(word in question_lower for word in ['compare', 'difference', 'vs', 'versus', 'better']):
            return self._compare_algorithms(question_lower)
        
        # Match against knowledge base
        best_match = self._find_best_match(question_lower)
        
        if best_match:
            answer = self.knowledge_base[best_match]['info']
        else:
            answer = self._generate_fallback_response(question_lower)
        
        # Store response
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'answer': answer,
            'type': 'assistant',
            'matched_topic': best_match
        })
        
        return answer
    
    def _find_best_match(self, question):
        """Find best matching topic"""
        scores = {}
        
        for topic, data in self.knowledge_base.items():
            score = sum(1 for keyword in data['keywords'] if keyword in question)
            if score > 0:
                scores[topic] = score
        
        if scores:
            return max(scores, key=scores.get)
        return None
    
    def _explain_how_it_works(self, question):
        """Explain how something works"""
        if 'kyber' in question:
            return """Kyber works using lattice-based cryptography:

1. **Key Generation**: Creates a "noisy" lattice structure
2. **Encryption**: Hides your message in the lattice with random noise
3. **Decryption**: Uses secret knowledge to remove noise and extract message

Why quantum computers can't break it:
- Quantum computers are good at factoring (breaks RSA)
- Quantum computers are NOT good at solving lattice problems
- The "Shortest Vector Problem" in high dimensions remains hard even for quantum computers

Think of it like hiding a needle in a haystack where quantum computers have no better tools 
than classical computers to find it!"""
        
        elif 'rsa' in question:
            return """RSA works using number theory:

1. **Key Generation**: Pick two large prime numbers (p, q), multiply them to get N
2. **Public Key**: N and a small number e (everyone can see this)
3. **Private Key**: The original primes p and q (kept secret)
4. **Encryption**: Math operation using public key
5. **Decryption**: Math operation that requires knowing p and q

Why quantum computers WILL break it:
- Security relies on: factoring N back into p × q is hard
- Classical computer: Would take millions of years
- Quantum computer with Shor's algorithm: Just 8 hours!"""
        
        else:
            return self._find_best_match_info(question)
    
    def _explain_why(self, question):
        """Answer 'why' questions"""
        if 'quantum' in question and 'threat' in question:
            return """The quantum threat is urgent for three reasons:

1. **"Harvest Now, Decrypt Later"**: Adversaries are stealing encrypted data TODAY to 
   decrypt when quantum computers arrive (2029-2030)

2. **Long-Term Data**: If you encrypted something in 2020 that needs to stay secret until 
   2035, it's already at risk!

3. **Migration Takes Time**: Moving an entire organization to PQC takes 1-2 years. 
   If you start in 2029, you'll finish in 2031 - too late!

That's why NIST and governments are pushing for migration NOW, even though quantum 
computers aren't quite ready yet."""
        
        elif 'faster' in question or 'speed' in question:
            return """Kyber is faster than RSA because:

1. **Simpler Math**: Lattice operations are more straightforward than modular exponentiation
2. **No Large Prime Generation**: RSA needs to find huge primes (slow), Kyber doesn't
3. **Modern Algorithm**: Designed in 2020s with efficiency in mind, not 1970s like RSA
4. **Better Parallelization**: Lattice operations work well on modern CPUs

The result: Kyber is 6,515x faster at key generation while being MORE secure!"""
        
        else:
            return self._find_best_match_info(question)
    
    def _explain_what(self, question):
        """Answer 'what' questions"""
        return self._find_best_match_info(question)
    
    def _give_recommendation(self, question):
        """Give recommendations"""
        if 'start' in question or 'begin' in question:
            return """Recommended Action Plan:

**Immediate (This Week):**
1. Run the migration assessment tool on your codebase
2. Identify systems using RSA/ECC encryption
3. Calculate risk scores for sensitive data

**Short Term (1-3 Months):**
1. Deploy hybrid mode for critical systems
2. Begin training development team on PQC
3. Update key management infrastructure

**Medium Term (6-12 Months):**
1. Full PQC deployment for high-value data
2. Migrate non-critical systems
3. Regular security audits

**Long Term (Ongoing):**
1. Monitor quantum computing progress
2. Stay updated on new PQC standards
3. Continuous testing and validation

The key: START NOW! Even small steps today prevent crisis in 2030."""
        
        elif 'algorithm' in question or 'choose' in question:
            return """Algorithm Selection Guide:

**Use Kyber-768 when:**
- ✅ Protecting data beyond 2030
- ✅ Need fastest performance
- ✅ Quantum safety is priority
- ✅ Building new systems

**Use RSA-2048 when:**
- ✅ Legacy system compatibility required
- ✅ Short-term data (expires before 2029)
- ✅ Regulatory compliance mandates it

**Use Hybrid Mode when:**
- ✅ In transition period (NOW!)
- ✅ Maximum security needed
- ✅ Supporting mixed environments
- ✅ Want belt-and-suspenders protection

Recommendation: Hybrid mode for 2026-2030, then pure Kyber."""
        
        else:
            return self._find_best_match_info(question)
    
    def _compare_algorithms(self, question):
        """Compare algorithms"""
        return """**Kyber-768 vs RSA-2048 Comparison:**

| Feature | Kyber-768 | RSA-2048 |
|---------|-----------|----------|
| **Quantum Safe** | ✅ Yes | ❌ No (broken by 2030) |
| **Key Gen Speed** | 0.03ms | 205ms (6515x slower!) |
| **Encryption Speed** | 0.015ms | 0.3ms (21x slower) |
| **Decryption Speed** | 0.01ms | 0.7ms (67x slower) |
| **Key Size** | 1184 bytes | 450 bytes |
| **Security Level** | 192-bit | 112-bit |
| **NIST Standard** | ✅ Yes (2024) | ✅ Yes (legacy) |
| **Industry Adoption** | Growing rapidly | Widespread (legacy) |

**Bottom Line**: Kyber is faster, more secure, and quantum-safe. The only reason to use 
RSA is backward compatibility. Use hybrid mode during transition!"""
    
    def _find_best_match_info(self, question):
        """Get info from best match"""
        match = self._find_best_match(question)
        if match:
            return self.knowledge_base[match]['info']
        return self._generate_fallback_response(question)
    
    def _generate_fallback_response(self, question):
        """Generate fallback for unknown questions"""
        return """I'm not sure about that specific question, but I can help with:

- How Kyber-768 and RSA-2048 work
- Why quantum computers threaten current encryption
- When RSA will be broken (timeline predictions)
- Migration strategies and recommendations
- Performance comparisons
- NIST standards and approval process

Try asking something like:
- "How does Kyber work?"
- "When will RSA be broken?"
- "What should I do to protect my data?"
- "Why is Kyber faster than RSA?"
- "Compare Kyber and RSA"

What would you like to know?"""

def demo():
    """Demo the AI assistant"""
    print("="*70)
    print("🤖 AI CRYPTO ASSISTANT DEMO")
    print("="*70)
    
    assistant = CryptoAssistant()
    
    test_questions = [
        "How does Kyber work?",
        "When will RSA be broken?",
        "Why is the quantum threat urgent?",
        "What should I do to migrate?",
        "Compare Kyber and RSA",
        "Why is Kyber faster?",
    ]
    
    for question in test_questions:
        print(f"\n❓ User: {question}")
        print("-"*70)
        answer = assistant.answer_question(question)
        print(f"🤖 Assistant:\n{answer}")
        print()
    
    print("="*70)
    print("Conversation History: {} exchanges".format(len(assistant.conversation_history) // 2))
    print("="*70)

if __name__ == "__main__":
    demo()
