#!/usr/bin/env python3
"""
Real-Time AI Assistant using Groq LLM
"""

import os
from dotenv import load_dotenv

load_dotenv()

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

class RealTimeAIAssistant:
    """Real AI assistant powered by Groq LLM"""
    
    def __init__(self, api_key=None):
        if not GROQ_AVAILABLE:
            self.enabled = False
            return
            
        self.api_key = (
            api_key or 
            os.environ.get('GROQ_API_KEY') or
            os.getenv('GROQ_API_KEY')
        )
        
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                # Use the new working model
                self.models = ["llama-3.3-70b-versatile", "llama3-8b-8192", "mixtral-8x7b-32768"]
                self.model = self.models[0]
                self.enabled = True
                print(f"✅ Groq AI enabled with model: {self.model}")
            except Exception as e:
                self.enabled = False
                print(f"❌ Groq initialization failed: {e}")
        else:
            self.enabled = False
        
        self.system_prompt = """You are QBits AI Assistant, an expert in post-quantum cryptography, 
quantum computing, and cybersecurity. Provide clear, accurate, concise answers (2-4 paragraphs).
Specialize in: CRYSTALS-Kyber, quantum threats, RSA vulnerabilities, NIST standards, and migration strategies."""

        self.conversation_history = []
    
    def ask(self, question):
        """Ask the AI a question"""
        
        if not self.enabled:
            return self._fallback_response(question)
        
        last_error = None
        self.conversation_history.append({"role": "user", "content": question})
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

        for model in self.models:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        *self.conversation_history
                    ],
                    temperature=0.7,
                    max_tokens=600,
                    top_p=1
                )
                answer = response.choices[0].message.content
                self.conversation_history.append({"role": "assistant", "content": answer})
                self.model = model  # remember which model worked
                return answer
            except Exception as e:
                last_error = e
                print(f"❌ Groq model {model} failed: {e}")
                continue

        # All models failed — return error details so we can debug
        return f"⚠️ AI Error (all models failed). Last error: {last_error}. Please check your GROQ_API_KEY on Render."
    
    def _fallback_response(self, question):
        """Fallback responses"""
        q = question.lower()
        
        if 'kyber' in q and 'work' in q:
            return """Kyber-768 uses lattice-based cryptography. It creates a "noisy" lattice structure where:
1. Key Generation: Creates random lattice points with noise
2. Encryption: Hides messages by adding them to lattice points
3. Decryption: Removes noise using secret knowledge

Quantum computers can't efficiently solve the Shortest Vector Problem in high-dimensional lattices, making Kyber quantum-resistant."""

        elif 'rsa' in q and ('break' in q or 'when' in q):
            return """RSA-2048 will likely be broken by quantum computers around 2029-2030. Current quantum computers have ~1,386 qubits; breaking RSA-2048 requires ~4,096 logical qubits. The "harvest now, decrypt later" threat means adversaries are already collecting encrypted data for future decryption."""

        return """I'm in limited mode. I can help with: Kyber-768 mechanics, RSA vulnerabilities, quantum timelines, migration strategies. Ask a specific question about these topics!"""
    
    def clear_history(self):
        self.conversation_history = []

if __name__ == "__main__":
    assistant = RealTimeAIAssistant()
    print(f"AI Enabled: {assistant.enabled}")
    if assistant.enabled:
        print(assistant.ask("How does Kyber work?"))
