import time
import pandas as pd
import streamlit as st
import common, caesar, affine, vigenere, strength, number_theory as nt

FREQ = dict(zip("etaoinshrdlcumwfgypbvkjxqz",
                [12.7, 9.1, 8.2, 7.5, 7.0, 6.7, 6.3, 6.1, 6.0, 4.3, 4.0, 2.8, 2.8,
                 2.4, 2.4, 2.2, 2.0, 2.0, 1.9, 1.5, 1.0, 0.8, 0.15, 0.15, 0.10, 0.07]))

BIGRAMS = ["th", "he", "in", "er", "an", "re", "on", "at", "en", "nd", "ti", "es", "or", "te", "of",
           "ed", "is", "it", "al", "ar", "st", "to", "nt", "ng", "se", "ha", "as", "ou", "io", "le",
           "ve", "co", "me", "de", "hi", "ri", "ro", "ic", "ne", "ea", "ra", "ce", "ec", "ss", "ma"]

def score(t):
    t = t.lower()
    letters = "".join(c for c in t if "a" <= c <= "z")
    return sum(FREQ.get(c, 0) for c in letters) + 8 * sum(letters.count(b) for b in BIGRAMS)

common.setup("Attack Lab", "🔎")
t1, t2, t3 = st.tabs(["Brute force", "Frequency analysis", "Password strength"])

with t1:
    cipher = st.radio("Cipher to attack", ["Caesar", "Affine"], horizontal=True)
    ct = st.text_area("Ciphertext", "WKLV LV D VHFUHW PHVVDJH", height=80)
    if st.button("Attack", type="primary"):
        t0 = time.perf_counter()
        if cipher == "Caesar":
            cands = [(f"k = {k}", caesar.decrypt(ct, k)) for k in range(26)]
        else:
            cands = [(f"a = {a}, b = {b}", affine.decrypt(ct, a, b))
                     for a in range(1, 26) if nt.gcd(a, 26) == 1 for b in range(26)]
        dt = time.perf_counter() - t0
        best = max(cands, key=lambda c: score(c[1]))
        c1, c2 = st.columns(2)
        c1.metric("Keys tried", len(cands))
        c2.metric("Time", f"{dt * 1000:.2f} ms")
        st.success(f"Most likely: {best[0]} gives \"{best[1]}\"")
        st.caption("The best guess is picked by English letter and letter-pair frequencies, so it works best on longer text. The table lists every key.")
        st.dataframe([{"Key": k, "Decrypted text": t} for k, t in cands])

with t2:
    sample = st.text_area("Sample English text",
                          "Discrete mathematics is the study of mathematical structures that are countable or otherwise "
                          "distinct and separable. It includes logic, sets, relations, functions and counting, and it is "
                          "the foundation of computer science and cryptography.", height=130)
    shift = st.slider("Caesar shift", 1, 25, 3)
    vkey = st.text_input("Vigenère keyword", "lemon")
    letters = "abcdefghijklmnopqrstuvwxyz"

    def counts(t):
        t = t.lower()
        return [t.count(c) for c in letters]

    try:
        df = pd.DataFrame({"Plain": counts(sample),
                           "Caesar": counts(caesar.encrypt(sample, shift)),
                           "Vigenère": counts(vigenere.encrypt(sample, vkey))},
                          index=list(letters.upper()))
        st.bar_chart(df)
        st.caption("Caesar only moves the same bars to new positions, so the English spikes stay visible. Vigenère spreads them out, which is why it is harder to break.")
    except ValueError as err:
        st.error(str(err))

with t3:
    pw = st.text_input("Type a password to test", key="pw_test")
    if pw:
        size, bits = strength.analyse(pw)
        c1, c2, c3 = st.columns(3)
        c1.metric("Character pool", size)
        c2.metric("Length", len(pw))
        c3.metric("Entropy", f"{bits:.1f} bits")
        st.progress(min(bits / 100, 1.0), text=strength.label(bits))
        st.write(f"By the multiplication principle there are {size}^{len(pw)} possible passwords, about 2^{bits:.0f}.")
        st.write(f"Average time to guess at 10^9 guesses per second: **{strength.crack_time(bits)}**")