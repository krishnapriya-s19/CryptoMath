def xor_bytes(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("Key required")
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))