import streamlit as st
import common

common.setup("CryptoMath", "🔐")
st.subheader("Encryption built on Discrete Mathematics")
st.write("Encrypt and decrypt text and files, attack weak ciphers, and watch the maths work step by step.")

c1, c2 = st.columns(2)
with c1:
    st.page_link("pages/1_Encrypt_Decrypt.py", label="Encrypt & Decrypt", icon="🔐")
    st.caption("Eight methods for text, AES and ChaCha20 for files.")
    st.page_link("pages/2_Math_Lab.py", label="Math Lab", icon="📐")
    st.caption("Step-by-step Caesar, Affine and RSA, plus counting, sets and logic.")
    st.page_link("pages/3_Attack_Lab.py", label="Attack Lab", icon="🔎")
    st.caption("Brute-force weak ciphers, frequency analysis, password strength.")
with c2:
    st.page_link("pages/4_Benchmark.py", label="Benchmark", icon="⚡")
    st.caption("Compare the speed of every algorithm.")
    st.page_link("pages/5_Hash_Check.py", label="Hash & Integrity", icon="🧾")
    st.caption("SHA-256 file checks, file comparison, avalanche effect.")

st.divider()
st.subheader("Where the syllabus appears")
st.markdown("""
| Syllabus topic | In CryptoMath |
|---|---|
| Propositional logic, truth tables (Unit 1) | XOR cipher, XOR truth table and equivalence |
| Sets, cardinality, inclusion-exclusion (Unit 1 and 3) | Key spaces, units mod n, φ(n) by inclusion-exclusion |
| Equivalence relations (Unit 2) | Congruence mod n behind Caesar, Affine and RSA |
| Bijective functions (Unit 2) | Every cipher must be a bijection to be decryptable |
| Pigeonhole principle (Unit 2) | Hash collisions |
| Permutations, combinations (Unit 3) | Keyword counts, substitution key space 26! |
| Derangements (Unit 3) | Ciphers that map no letter to itself |
| Euler's phi function (Unit 3) | RSA and the Affine cipher key count |
""")