import time, base64
import streamlit as st
import caesar, vigenere, xor_cipher, rsa, aes

INFO = {
    "Caesar": ("26 shifts (~4.7 bits)", "Very weak"),
    "Vigenère": ("Keyword based", "Weak"),
    "XOR": ("Key length x 8 bits", "Weak (repeating key)"),
    "RSA": ("512-bit modulus (demo)", "Educational; real use needs 2048+"),
    "AES": ("256-bit", "Strong"),
}

def run(algo, enc, text, key):
    if algo == "Caesar":
        k = int(key)
        return caesar.encrypt(text, k) if enc else caesar.decrypt(text, k)
    if algo == "Vigenère":
        return vigenere.encrypt(text, key) if enc else vigenere.decrypt(text, key)
    if algo == "XOR":
        if enc:
            return xor_cipher.xor_bytes(text.encode(), key.encode()).hex()
        return xor_cipher.xor_bytes(bytes.fromhex(text), key.encode()).decode()
    if algo == "RSA":
        k = st.session_state.rsa
        return rsa.encrypt(text, k["n"], k["e"]) if enc else rsa.decrypt(text, k["n"], k["d"])
    if enc:
        return base64.b64encode(aes.encrypt(text.encode(), key)).decode()
    return aes.decrypt(base64.b64decode(text), key).decode()

def stats(algo, dt, label):
    st.write(f"⏱ **{label} time:** {dt * 1000:.2f} ms")
    st.write(f"🔑 **Key size:** {INFO[algo][0]}")
    st.write(f"🛡 **Security level:** {INFO[algo][1]}")

st.set_page_config(page_title="Secure Crypto", page_icon="🔐")
st.title("🔐 Secure File Encryption & Decryption")
tab1, tab2, tab3 = st.tabs(["Text", "File", "Math behind it"])

with tab1:
    algo = st.selectbox("Algorithm", list(INFO))
    mode = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True)
    text = st.text_area("Input")
    key = ""
    if algo == "RSA":
        if "rsa" not in st.session_state:
            st.session_state.rsa = rsa.generate_keys(512)
        k = st.session_state.rsa
        with st.expander("RSA keys (p, q, n, φ(n), e, d)"):
            st.write({x: k[x] for x in ("p", "q", "n", "phi", "e", "d")})
    else:
        key = st.text_input("Key (number for Caesar, word for Vigenère, password for XOR/AES)")
    if st.button("Run", key="run1"):
        try:
            t0 = time.perf_counter()
            out = run(algo, mode == "Encrypt", text, key)
            dt = time.perf_counter() - t0
            st.code(out, language=None)
            stats(algo, dt, mode + "ion" if mode == "Encrypt" else "Decryption")
        except Exception as e:
            st.error(f"Failed: {e}")

with tab2:
    f = st.file_uploader("Choose a file")
    pw = st.text_input("Password", type="password", key="filepw")
    mode2 = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True, key="m2")
    if f and pw and st.button("Run", key="run2"):
        try:
            data, enc = f.read(), mode2 == "Encrypt"
            t0 = time.perf_counter()
            out = aes.encrypt(data, pw) if enc else aes.decrypt(data, pw)
            dt = time.perf_counter() - t0
            name = f.name + ".enc" if enc else (f.name[:-4] if f.name.endswith(".enc") else "decrypted_" + f.name)
            st.success("Done")
            stats("AES", dt, "Encryption" if enc else "Decryption")
            st.download_button("Download result", out, file_name=name)
        except Exception as e:
            st.error("Failed: wrong password or corrupted file")

with tab3:
    st.markdown("""
| Syllabus topic | Where it appears |
|---|---|
| Euler's phi (Unit 3) | RSA: φ(n) = (p−1)(q−1) |
| Bijective functions (Unit 2) | Encrypt is a bijection, decrypt is its inverse |
| Equivalence relations (Unit 2) | Congruence mod n drives Caesar, Vigenère, RSA |
| Propositional logic (Unit 1) | XOR cipher and its truth table |
| Counting / permutations (Unit 3) | Key space: 26 Caesar keys, 2^256 for AES |
| Pigeonhole principle (Unit 2) | Why weak ciphers with small key spaces collide |
""")