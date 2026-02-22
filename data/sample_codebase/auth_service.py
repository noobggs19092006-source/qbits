
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
