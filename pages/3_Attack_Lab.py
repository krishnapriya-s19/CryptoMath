
import time
import pandas as pd
import streamlit as st

import common
import caesar
import affine
import vigenere
import strength
import number_theory as nt


# PAGE SETUP
common.setup("Attack Lab", "🔎")

st.title("Attack Lab")
st.caption("Explore classical cipher weaknesses and cryptographic security.")

st.divider()

# ENGLISH FREQUENCY DATA
FREQ = dict(zip(
    "etaoinshrdlcumwfgypbvkjxqz",
    [
        12.7, 9.1, 8.2, 7.5, 7.0, 6.7, 6.3, 6.1,
        6.0, 4.3, 4.0, 2.8, 2.8, 2.4, 2.4, 2.2,
        2.0, 2.0, 1.9, 1.5, 1.0, 0.8, 0.15,
        0.15, 0.10, 0.07
    ]
))

BIGRAMS = [
    "th", "he", "in", "er", "an", "re", "on",
    "at", "en", "nd", "ti", "es", "or", "te",
    "of", "ed", "is", "it", "al", "ar", "st",
    "to", "nt", "ng", "se", "ha", "as", "ou",
    "io", "le", "ve", "co", "me", "de", "hi",
    "ri", "ro", "ic", "ne", "ea", "ra", "ce",
    "ec", "ss", "ma"
]


def english_score(text):
    text = text.lower()
    letters = "".join(c for c in text if "a" <= c <= "z")

    letter_score = sum(FREQ.get(c, 0) for c in letters)
    bigram_score = 8 * sum(letters.count(b) for b in BIGRAMS)

    return letter_score + bigram_score


def count_letters(text):
    text = text.lower()
    return [text.count(c) for c in "abcdefghijklmnopqrstuvwxyz"]


# TABS
tab1, tab2, tab3 = st.tabs([
    "Brute Force",
    "Frequency Analysis",
    "Password Strength"
])


# ==================================================
# TAB 1 - BRUTE FORCE
# ==================================================

with tab1:
    st.subheader("Classical Cipher Analysis")
    st.write(
        "Explore how a limited number of possible keys "
        "makes classical ciphers vulnerable to exhaustive testing."
    )

    cipher = st.radio(
        "Select cipher",
        ["Caesar", "Affine"],
        horizontal=True,
        key="attack_cipher"
    )

    if cipher == "Caesar":
        st.latex(r"C = (P + k) \bmod 26")
        st.caption("Caesar has 26 possible shift keys.")

    else:
        st.latex(r"E(x) = (ax+b) \bmod 26")
        st.caption("Affine has 312 valid key combinations.")

    ciphertext = st.text_area(
        "Enter ciphertext",
        value="WKLV LV D VHFUHW PHVVDJH",
        height=100,
        key="attack_ciphertext"
    )

    if st.button("Run Analysis", type="primary", key="run_attack"):
        if not ciphertext.strip():
            st.warning("Enter some ciphertext first.")

        else:
            start = time.perf_counter()

            if cipher == "Caesar":
                candidates = [
                    (f"k = {k}", caesar.decrypt(ciphertext, k))
                    for k in range(26)
                ]

            else:
                candidates = [
                    (
                        f"a = {a}, b = {b}",
                        affine.decrypt(ciphertext, a, b)
                    )
                    for a in range(1, 26)
                    if nt.gcd(a, 26) == 1
                    for b in range(26)
                ]

            elapsed = time.perf_counter() - start

            best = max(
                candidates,
                key=lambda item: english_score(item[1])
            )

            st.session_state["attack_results"] = {
                "cipher": cipher,
                "candidates": candidates,
                "best": best,
                "elapsed": elapsed
            }

    result = st.session_state.get("attack_results")

    if result and result["cipher"] == cipher:
        st.divider()
        st.subheader("Analysis Results")

        c1, c2, c3 = st.columns(3)

        c1.metric("Keys evaluated", len(result["candidates"]))
        c2.metric("Execution time", f"{result['elapsed'] * 1000:.3f} ms")
        c3.metric("Most likely key", result["best"][0])

        st.success("Most likely plaintext: " + result["best"][1])

        st.caption(
            "The most likely result is estimated using English "
            "letter and letter-pair frequencies. It is not guaranteed "
            "to be the correct plaintext."
        )

        with st.expander("View all candidate results"):
            candidate_rows = []

            for key, plaintext in result["candidates"]:
                candidate_rows.append({
                    "Key": key,
                    "Decrypted text": plaintext,
                    "English score": round(english_score(plaintext), 2)
                })

            candidate_rows.sort(
                key=lambda item: item["English score"],
                reverse=True
            )

            st.dataframe(
                candidate_rows,
                use_container_width=True,
                hide_index=True
            )


# ==================================================
# TAB 2 - FREQUENCY ANALYSIS
# ==================================================

with tab2:
    st.subheader("Letter Frequency Analysis")

    st.write(
        "Compare letter distributions in original text "
        "and encrypted text."
    )

    sample = st.text_area(
        "Enter sample English text",
        value=(
            "Discrete mathematics is the study of mathematical "
            "structures that are countable or otherwise distinct "
            "and separable. It includes logic, sets, relations, "
            "functions and counting, and it is the foundation "
            "of computer science and cryptography."
        ),
        height=140,
        key="frequency_sample"
    )

    c1, c2 = st.columns(2)

    with c1:
        shift = st.slider(
            "Caesar shift",
            1,
            25,
            3,
            key="frequency_shift"
        )

    with c2:
        keyword = st.text_input(
            "Vigenere keyword",
            "lemon",
            key="frequency_keyword"
        )

    if st.button(
        "Compare Frequencies",
        type="primary",
        key="compare_frequency"
    ):
        if not sample.strip():
            st.warning("Enter some sample text.")

        elif not keyword.strip():
            st.warning("Enter a Vigenere keyword.")

        else:
            try:
                caesar_text = caesar.encrypt(sample, shift)
                vigenere_text = vigenere.encrypt(sample, keyword)

                df = pd.DataFrame(
                    {
                        "Original": count_letters(sample),
                        "Caesar": count_letters(caesar_text),
                        "Vigenere": count_letters(vigenere_text)
                    },
                    index=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                )

                st.session_state["frequency_results"] = {
                    "data": df,
                    "caesar": caesar_text,
                    "vigenere": vigenere_text
                }

            except ValueError as error:
                st.error(str(error))

    frequency_result = st.session_state.get("frequency_results")

    if frequency_result:
        st.divider()
        st.subheader("Frequency Distribution")

        st.bar_chart(
            frequency_result["data"],
            use_container_width=True
        )

        with st.expander("View encrypted text"):
            st.markdown("**Caesar ciphertext**")
            st.code(frequency_result["caesar"])

            st.markdown("**Vigenere ciphertext**")
            st.code(frequency_result["vigenere"])

        st.markdown("#### Understanding the results")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**Caesar Cipher**")
            st.write(
                "Every letter is shifted by the same amount. "
                "The frequency pattern remains, but the letters "
                "occupying each position change."
            )

        with c2:
            st.markdown("**Vigenere Cipher**")
            st.write(
                "Different shifts are applied using a keyword. "
                "This spreads letter frequencies and makes simple "
                "frequency analysis less effective."
            )


# ==================================================
# TAB 3 - PASSWORD STRENGTH
# ==================================================

with tab3:
    st.subheader("Password Strength Estimator")

    st.info(
        "Use a sample password for this demonstration. "
        "Do not enter a password used for a personal account."
    )

    password = st.text_input(
        "Enter a sample password",
        type="password",
        key="sample_password"
    )

    if password:
        size, bits = strength.analyse(password)

        st.divider()

        c1, c2, c3 = st.columns(3)

        c1.metric("Character pool", size)
        c2.metric("Password length", len(password))
        c3.metric("Estimated entropy", f"{bits:.1f} bits")

        st.markdown("#### Estimated strength")

        st.progress(
            min(bits / 100, 1.0),
            text=strength.label(bits)
        )

        st.markdown("#### Mathematical explanation")

        st.latex(r"H = L \times \log_2(S)")

        st.write(f"Character pool (S): **{size}**")
        st.write(f"Password length (L): **{len(password)}**")
        st.write(f"Estimated entropy: **{bits:.2f} bits**")

        st.latex(r"\text{Possible combinations} = S^L")

        st.markdown("#### Illustrative guessing-time estimate")

        st.metric(
            "Estimated average time",
            strength.crack_time(bits)
        )

        st.caption(
            "This is a simplified theoretical estimate. "
            "Actual security depends on password patterns, "
            "hashing methods and other protections."
        )

    else:
        st.write("Enter a sample password to view its analysis.")


# FOOTER
st.divider()
st.caption("CRYPTOMATH | ATTACK LAB")
