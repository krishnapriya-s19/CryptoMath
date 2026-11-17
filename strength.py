import math
import string

def analyse(pw):
    """Return (character pool size, entropy in bits)."""
    size = 0
    if any(c in string.ascii_lowercase for c in pw):
        size += 26
    if any(c in string.ascii_uppercase for c in pw):
        size += 26
    if any(c in string.digits for c in pw):
        size += 10
    if any(c not in string.ascii_letters + string.digits for c in pw):
        size += 33
    bits = len(pw) * math.log2(size) if size else 0.0
    return size, bits

def label(bits):
    if bits < 28:
        return "Very weak"
    if bits < 36:
        return "Weak"
    if bits < 60:
        return "Fair"
    if bits < 80:
        return "Strong"
    return "Very strong"

def crack_time(bits, rate=1e9):
    seconds = 2.0 ** (min(bits, 1000) - 1) / rate
    if seconds < 1:
        return "instantly"
    for name, s in (("years", 31_557_600), ("days", 86_400), ("hours", 3_600), ("minutes", 60)):
        if seconds >= s:
            return f"{seconds / s:.3g} {name}"
    return f"{seconds:.3g} seconds"