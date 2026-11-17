import streamlit as st
import common, hashing

common.setup("Hash and Integrity", "🧾")
t1, t2, t3 = st.tabs(["Hash a file", "Compare two files", "Avalanche effect"])

with t1:
    f = st.file_uploader("Choose a file", key="h1")
    if f:
        h = hashing.sha256_hex(f.getvalue())
        st.code(h, language=None)
        expected = st.text_input("Expected SHA-256 (optional)", key="expected").strip().lower()
        if expected:
            if expected == h:
                st.success("Match: the file is unchanged.")
            else:
                st.error("No match: the file has changed.")
    st.caption("Tip: hash a file, encrypt it, decrypt it, then hash again. Same hash means nothing was lost.")

with t2:
    fa = st.file_uploader("First file", key="h2a")
    fb = st.file_uploader("Second file", key="h2b")
    if fa and fb:
        ha, hb = hashing.sha256_hex(fa.getvalue()), hashing.sha256_hex(fb.getvalue())
        st.code(f"{fa.name}: {ha}\n{fb.name}: {hb}", language=None)
        if ha == hb:
            st.success("The files are identical.")
        else:
            st.error("The files are different.")

with t3:
    a = st.text_input("Text A", "hello world", key="av_a")
    b = st.text_input("Text B (change one character)", "hello worle", key="av_b")
    diff = hashing.avalanche(a, b)
    st.code(f"A: {hashing.sha256_hex(a.encode())}\nB: {hashing.sha256_hex(b.encode())}", language=None)
    st.metric("Bits that differ", f"{diff} / 256")
    st.progress(diff / 256)
    st.caption("Changing one character flips about half of the 256 bits. A hash is not a bijection: unlimited inputs share 2^256 outputs, so collisions exist by the pigeonhole principle, but finding one is infeasible.")