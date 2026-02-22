
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
