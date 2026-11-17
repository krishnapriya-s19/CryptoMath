import base64
import streamlit as st
import caesar, affine, vigenere, xor_cipher, otp, rsa, aes, chacha

INFO = {
    "Caesar": ("26 keys", "Very weak"),
    "Affine": ("312 keys", "Very weak"),
    "Vigenère": ("26^k keys", "Weak"),
    "XOR": ("8 × key bytes", "Weak"),
    "One-Time Pad": ("= message length", "Perfect*"),
    "RSA": ("512-bit", "Demo only"),
    "ChaCha20": ("256-bit", "Strong"),
    "AES": ("256-bit", "Strong"),
}
NOTES = {
    "XOR": "A short repeating key is easy to break.",
    "One-Time Pad": "*Perfect secrecy only if the key is truly random, as long as the message, and never reused.",
    "RSA": "512-bit RSA is for learning. Real RSA uses 2048+ bits and padding.",
    "Vigenère": "k is the keyword length. Longer keywords mean more keys.",
}
KEY_HINT = {
    "Caesar": "A whole number, e.g. 3",
    "Affine": "Two numbers a,b e.g. 5,8 (a must be coprime with 26)",
    "Vigenère": "A word, e.g. lemon",
    "XOR": "Any text",
    "One-Time Pad": "Hex key at least as long as the message (use the button)",
    "AES": "A password",
    "ChaCha20": "A password",
}
TEXT_ALGOS = list(INFO)
FILE_ALGOS = ["AES", "ChaCha20"]

CSS = """
<style>
div[data-testid="stMetric"] {background:#181B22; border:1px solid #2A2F3A; padding:14px 16px; border-radius:12px;}
.stButton>button, .stDownloadButton>button {border-radius:10px; font-weight:600;}
.block-container {padding-top: 2rem;}
</style>
"""

def setup(title, icon):
    st.set_page_config(page_title=f"CryptoMath | {title}", page_icon=icon, layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    st.sidebar.caption("CryptoMath · Discrete Mathematics project")
    st.title(f"{icon} {title}")

def _int(text, msg):
    try:
        return int(text)
    except ValueError:
        raise ValueError(msg) from None

def run_text(algo, enc, text, key, rsa_keys=None):
    if algo == "Caesar":
        k = _int(key, "Caesar key must be a whole number, e.g. 3")
        return caesar.encrypt(text, k) if enc else caesar.decrypt(text, k)
    if algo == "Affine":
        parts = key.split(",")
        if len(parts) != 2:
            raise ValueError("Affine key must look like 5,8")
        a, b = (_int(x, "Affine key must look like 5,8") for x in parts)
        return affine.encrypt(text, a, b) if enc else affine.decrypt(text, a, b)
    if algo == "Vigenère":
        return vigenere.encrypt(text, key) if enc else vigenere.decrypt(text, key)
    if algo == "XOR":
        if enc:
            return xor_cipher.xor_bytes(text.encode(), key.encode()).hex()
        return xor_cipher.xor_bytes(bytes.fromhex(text), key.encode()).decode()
    if algo == "One-Time Pad":
        return otp.encrypt(text, key) if enc else otp.decrypt(text, key)
    if algo == "RSA":
        if enc:
            return rsa.encrypt(text, rsa_keys["n"], rsa_keys["e"])
        return rsa.decrypt(text, rsa_keys["n"], rsa_keys["d"])
    mod = aes if algo == "AES" else chacha
    if enc:
        return base64.b64encode(mod.encrypt(text.encode(), key)).decode()
    return mod.decrypt(base64.b64decode(text), key).decode()

def show_stats(algo, dt, enc):
    size, level = INFO[algo]
    c1, c2, c3 = st.columns(3)
    c1.metric("Encryption time" if enc else "Decryption time", f"{dt * 1000:.2f} ms")
    c2.metric("Key size", size)
    c3.metric("Security level", level)
    if NOTES.get(algo):
        st.caption(NOTES[algo])