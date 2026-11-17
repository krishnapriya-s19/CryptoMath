import os

def generate_key(n_bytes):
    return os.urandom(max(n_bytes, 1)).hex()

def _xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def encrypt(text, key_hex):
    data, key = text.encode(), bytes.fromhex(key_hex)
    if len(key) < len(data):
        raise ValueError("Key must be at least as long as the message")
    return _xor(data, key).hex()

def decrypt(cipher_hex, key_hex):
    data, key = bytes.fromhex(cipher_hex), bytes.fromhex(key_hex)
    if len(key) < len(data):
        raise ValueError("Key must be at least as long as the message")
    return _xor(data, key).decode()