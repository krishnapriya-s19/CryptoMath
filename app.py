
import streamlit as st
import common


# ==================================================
# PAGE SETUP
# ==================================================

common.setup("Home", "🔐")


# ==================================================
# HERO SECTION
# ==================================================

st.markdown("### DISCRETE MATHEMATICS × CRYPTOGRAPHY")

st.subheader(
    "Secure your data. Understand the mathematics."
)

st.write(
    "CryptoMath is an interactive learning platform that connects "
    "cryptographic algorithms with the mathematical concepts behind them."
)

st.write("")

# Quick statistics
c1, c2, c3 = st.columns(3)

c1.metric("Algorithms", "8")
c2.metric("Learning Labs", "5")
c3.metric("Core Subject", "Discrete Mathematics")

st.divider()


# ==================================================
# PLATFORM OVERVIEW
# ==================================================

st.header("Explore CryptoMath")

st.write(
    "Choose a workspace to explore its features."
)

col1, col2 = st.columns(2, gap="large")


with col1:

    with st.container(border=True):
        st.subheader("🔐 Encrypt & Decrypt")

        st.write(
            "Encrypt and decrypt messages using eight different "
            "cryptographic algorithms."
        )

        st.caption(
            "Caesar · Affine · Vigenère · XOR · OTP · RSA · AES · ChaCha20"
        )

        st.page_link(
            "pages/1_Encrypt_Decrypt.py",
            label="Open Encryption Lab",
            icon="🔐",
            use_container_width=True
        )

    with st.container(border=True):
        st.subheader("📐 Math Lab")

        st.write(
            "Understand the mathematical principles behind "
            "cryptographic algorithms."
        )

        st.caption(
            "Number theory · RSA mathematics · Counting · Logic · Sets"
        )

        st.page_link(
            "pages/2_Math_Lab.py",
            label="Open Math Lab",
            icon="📐",
            use_container_width=True
        )

    with st.container(border=True):
        st.subheader("🔎 Attack Lab")

        st.write(
            "Explore the weaknesses of classical ciphers and "
            "understand password strength."
        )

        st.caption(
            "Brute force · Frequency analysis · Password entropy"
        )

        st.page_link(
            "pages/3_Attack_Lab.py",
            label="Open Attack Lab",
            icon="🔎",
            use_container_width=True
        )


with col2:

    with st.container(border=True):
        st.subheader("⚡ Performance Benchmark")

        st.write(
            "Compare encryption and decryption performance "
            "across different algorithms."
        )

        st.caption(
            "Execution time · Key generation · Performance comparison"
        )

        st.page_link(
            "pages/4_Benchmark.py",
            label="Open Benchmark",
            icon="⚡",
            use_container_width=True
        )

    with st.container(border=True):
        st.subheader("🧾 Hash & Integrity")

        st.write(
            "Generate SHA-256 hashes, compare files and "
            "understand the avalanche effect."
        )

        st.caption(
            "SHA-256 · File verification · Hash comparison"
        )

        st.page_link(
            "pages/5_Hash_Check.py",
            label="Open Hash Lab",
            icon="🧾",
            use_container_width=True
        )

    with st.container(border=True):
        st.subheader("📚 About This Project")

        st.write(
            "CryptoMath demonstrates how discrete mathematics "
            "is applied in computer security and cryptography."
        )

        st.caption(
            "An interactive Discrete Mathematics project."
        )


st.divider()


# ==================================================
# MATHEMATICS CONNECTION
# ==================================================

st.header("Where Mathematics Meets Cryptography")

st.write(
    "The project connects important Discrete Mathematics "
    "topics with practical cryptographic applications."
)

math_data = [
    {
        "Mathematical Concept": "Propositional Logic",
        "Application in CryptoMath": "XOR operations and truth tables"
    },
    {
        "Mathematical Concept": "Sets and Cardinality",
        "Application in CryptoMath": "Cryptographic key spaces"
    },
    {
        "Mathematical Concept": "Equivalence Relations",
        "Application in CryptoMath": "Congruence modulo n"
    },
    {
        "Mathematical Concept": "Bijective Functions",
        "Application in CryptoMath": "Reversible encryption functions"
    },
    {
        "Mathematical Concept": "Pigeonhole Principle",
        "Application in CryptoMath": "Hash collisions"
    },
    {
        "Mathematical Concept": "Permutations and Combinations",
        "Application in CryptoMath": "Possible encryption keys"
    },
    {
        "Mathematical Concept": "Euler's Totient Function",
        "Application in CryptoMath": "RSA and Affine cipher"
    },
    {
        "Mathematical Concept": "Number Theory",
        "Application in CryptoMath": "Prime numbers, GCD and modular arithmetic"
    }
]

st.dataframe(
    math_data,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# ALGORITHM OVERVIEW
# ==================================================

st.divider()

st.header("Cryptographic Algorithms")

st.write(
    "CryptoMath demonstrates classical and modern "
    "cryptographic techniques."
)

with st.expander("Classical Algorithms"):
    st.markdown("""
    - **Caesar Cipher:** Uses a fixed alphabet shift.
    - **Affine Cipher:** Uses modular multiplication and addition.
    - **Vigenère Cipher:** Uses a repeating keyword.
    - **XOR Cipher:** Uses bitwise exclusive OR.
    - **One-Time Pad:** Demonstrates the principle of perfect secrecy.
    """)

with st.expander("Modern Algorithms"):
    st.markdown("""
    - **RSA:** Public-key cryptography based on number theory.
    - **AES:** Symmetric-key encryption.
    - **ChaCha20:** Stream cipher based on modular arithmetic and bitwise operations.
    """)

with st.expander("Hashing and Integrity"):
    st.markdown("""
    - **SHA-256:** Generates a fixed-length cryptographic hash.
    - **File Verification:** Compares file hashes to check integrity.
    - **Avalanche Effect:** Demonstrates how small input changes affect hash output.
    """)


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "🔐 CRYPTOMATH | Discrete Mathematics Project"
)

st.caption(
    "Explore. Experiment. Understand."
)
