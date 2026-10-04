def _run(text, key, sign):
    shifts = [ord(c.lower()) - 97 for c in key if c.isascii() and c.isalpha()]
    if not shifts:
        raise ValueError("Key must contain letters")
    out, i = [], 0
    for ch in text:
        if ch.isascii() and ch.isalpha():
            base = 65 if ch.isupper() else 97
            out.append(chr((ord(ch) - base + sign * shifts[i % len(shifts)]) % 26 + base))
            i += 1
        else:
            out.append(ch)
    return "".join(out)

def encrypt(text, key):
    return _run(text, key, 1)

def decrypt(text, key):
    return _run(text, key, -1)