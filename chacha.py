  
import os

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


# Generate a 256-bit encryption key from the user's password.
def _key(password: str, salt: bytes) -> bytes:
    if not password:
        raise ValueError("Password cannot be empty.")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000
    )

    return kdf.derive(password.encode("utf-8"))


# Encrypt data using ChaCha20-Poly1305.
def encrypt(data: bytes, password: str) -> bytes:
    salt = os.urandom(16)
    nonce = os.urandom(12)

    key = _key(password, salt)

    cipher = ChaCha20Poly1305(key)

    ciphertext = cipher.encrypt(nonce, data, None)

    # Store salt + nonce + ciphertext together.
    return salt + nonce + ciphertext


# Decrypt data using the same password.
def decrypt(blob: bytes, password: str) -> bytes:
    if len(blob) < 44:
        raise ValueError("Invalid or corrupted encrypted data.")

    salt = blob[:16]
    nonce = blob[16:28]
    ciphertext = blob[28:]

    key = _key(password, salt)

    cipher = ChaCha20Poly1305(key)

    try:
        return cipher.decrypt(nonce, ciphertext, None)
    except Exception:
        raise ValueError(
            "Decryption failed. Wrong password or corrupted data."
        ) from None
