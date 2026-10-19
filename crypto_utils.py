import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

iter = 600_000 #OWASP Password Stroage recommended iterations for use in PBKDF2 key derivation

def keySalt() -> bytes:
    """random value that makes every vault's key different
     salt is a random value mixed into the key derivation"""
    return os.urandom(16) #secure 16 bytes random bytes

def deriveKey(masterPassword: str, salt: bytes) -> bytes:
    """takes the master password string and the salt 
    then encode the text to bytes. Same password and salt always gives the same key.
    The purpose of this function is to make the master key not a stored object it is derived from password and a random salt"""
    keyDerivationFunction = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iter)
    return base64.urlsafe_b64decode(keyDerivationFunction(masterPassword.encode()))

def encrypt(data: bytes, key: bytes) ->bytes:
    """encrypt data using fernet from cryptography 
    library that uses AES encryption + an integrity check.
    The result is a token ciphertect + timestamp to ensure integrity"""
    return Fernet(key).encrypt(data)

def decrypt(token: bytes, key: bytes) ->bytes:
    """Reverses encrypt function"""
    return Fernet(key).decrypt(token) #raises invalidToken if key is wrong