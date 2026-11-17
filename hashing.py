import hashlib

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def avalanche(a: str, b: str) -> int:
    """Number of bits (out of 256) that differ between the hashes of a and b."""
    ha = int(sha256_hex(a.encode()), 16)
    hb = int(sha256_hex(b.encode()), 16)
    return bin(ha ^ hb).count("1")