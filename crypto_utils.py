import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

iter = 600_000 #iterations to make it harder for attacker

def keySalt() -> bytes:
    """random value that makes every vault's key different"""
    return os.urandom(16) #secure 16 bytes random bytes

def deriveKey(masterPassword: str, salt: bytes) -> bytes:
    keyDerivationFunction = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iter)
    return base64.urlsafe_b64decode(keyDerivationFunction(masterPassword.encode()))

def encrypt(data: bytes, key: bytes) ->bytes:
    return Fernet(key).encrypt(data)