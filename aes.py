import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def _key(password, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=200_000)
    return kdf.derive(password.encode())

def encrypt(data: bytes, password: str) -> bytes:
    salt, nonce = os.urandom(16), os.urandom(12)
    return salt + nonce + AESGCM(_key(password, salt)).encrypt(nonce, data, None)

def decrypt(blob: bytes, password: str) -> bytes:
    if len(blob) < 44:
        raise ValueError("Not valid encrypted data")
    salt, nonce, ct = blob[:16], blob[16:28], blob[28:]
    return AESGCM(_key(password, salt)).decrypt(nonce, ct, None)  # wrong password -> error