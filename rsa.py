import json
from number_theory import generate_prime, gcd, mod_inverse, mod_exp

def generate_keys(bits=512):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    while q == p:
        q = generate_prime(bits // 2)
    n, phi = p * q, (p - 1) * (q - 1)
    e = 65537
    while gcd(e, phi) != 1:
        e += 2
    d = mod_inverse(e, phi)
    return {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d}

def _size(n):
    return (n.bit_length() - 1) // 8 - 1

def encrypt(text, n, e):
    data, s = text.encode(), _size(n)
    chunks = [data[i:i + s] for i in range(0, len(data), s)]
    return ",".join(str(mod_exp(int.from_bytes(b"\x01" + c, "big"), e, n)) for c in chunks)

def decrypt(cipher, n, d):
    out = b""
    for c in cipher.split(","):
        m = mod_exp(int(c), d, n)
        out += m.to_bytes((m.bit_length() + 7) // 8, "big")[1:]
    return out.decode()

def export_keys(keys):
    return json.dumps({k: str(v) for k, v in keys.items()}, indent=2)

def import_keys(text):
    try:
        keys = {k: int(v) for k, v in json.loads(text).items()}
        n, e, d = keys["n"], keys["e"], keys["d"]
        if mod_exp(mod_exp(2, e, n), d, n) != 2:
            raise ValueError
    except Exception:
        raise ValueError("Invalid RSA key file") from None
    return keys