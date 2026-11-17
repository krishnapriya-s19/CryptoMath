import time
import pandas as pd
import streamlit as st
import common, otp, rsa

common.setup("Benchmark", "⚡")
st.caption("Compare how fast each algorithm encrypts and decrypts the same message.")
size = st.slider("Message size (characters)", 100, 20000, 2000, step=100)

if st.button("Run benchmark", type="primary"):
    msg = ("The quick brown fox jumps over the lazy dog. " * (size // 40 + 1))[:size]
    with st.spinner("Running..."):
        t0 = time.perf_counter()
        rk = rsa.generate_keys(512)
        keygen_ms = (time.perf_counter() - t0) * 1000
        keys = {"Caesar": "3", "Affine": "5,8", "Vigenère": "lemon", "XOR": "key",
                "One-Time Pad": otp.generate_key(len(msg.encode())), "RSA": "",
                "ChaCha20": "benchmark-pw", "AES": "benchmark-pw"}
        rows = []
        for algo in common.TEXT_ALGOS:
            t0 = time.perf_counter()
            ct = common.run_text(algo, True, msg, keys[algo], rk)
            t1 = time.perf_counter()
            common.run_text(algo, False, ct, keys[algo], rk)
            t2 = time.perf_counter()
            rows.append({"Algorithm": algo,
                         "Encrypt (ms)": round((t1 - t0) * 1000, 2),
                         "Decrypt (ms)": round((t2 - t1) * 1000, 2),
                         "Key size": common.INFO[algo][0],
                         "Security": common.INFO[algo][1]})
    df = pd.DataFrame(rows)
    st.dataframe(df)
    st.bar_chart(df.set_index("Algorithm")[["Encrypt (ms)", "Decrypt (ms)"]])
    st.caption(f"RSA key generation took {keygen_ms:.0f} ms (not included above). AES and ChaCha20 times include PBKDF2 key derivation, which is slow on purpose to resist password guessing.")