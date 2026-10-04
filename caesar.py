def _shift(text, k):
    out = []
    for ch in text:
        if ch.isascii() and ch.isalpha():
            base = 65 if ch.isupper() else 97
            out.append(chr((ord(ch) - base + k) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)

def encrypt(text, k):
    return _shift(text, k)

def decrypt(text, k):
    return _shift(text, -k)