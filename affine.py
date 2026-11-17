from number_theory import gcd, mod_inverse

VALID_A = [a for a in range(1, 26) if gcd(a, 26) == 1]

def _check(a):
    if gcd(a, 26) != 1:
        raise ValueError(f"a must be coprime with 26. Valid values: {VALID_A}")

def _apply(text, f):
    out = []
    for ch in text:
        if ch.isascii() and ch.isalpha():
            base = 65 if ch.isupper() else 97
            out.append(chr(f(ord(ch) - base) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)

def encrypt(text, a, b):
    a, b = a % 26, b % 26
    _check(a)
    return _apply(text, lambda x: a * x + b)

def decrypt(text, a, b):
    a, b = a % 26, b % 26
    _check(a)
    inv = mod_inverse(a, 26)
    return _apply(text, lambda y: inv * (y - b))