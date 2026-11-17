
import base64
import streamlit as st

import caesar
import affine
import vigenere
import xor_cipher
import otp
import rsa
import aes
import chacha


# ==================================================
# ALGORITHM INFORMATION
# ==================================================

INFO = {
    "Caesar": ("26 keys", "Very weak"),
    "Affine": ("312 keys", "Very weak"),
    "Vigenère": ("26^k keys", "Weak"),
    "XOR": ("8 × key bytes", "Weak"),
    "One-Time Pad": ("Message length", "Perfect*"),
    "RSA": ("512-bit", "Demo only"),
    "ChaCha20": ("256-bit", "Strong"),
    "AES": ("256-bit", "Strong"),
}

NOTES = {
    "XOR": "A short repeating key is easy to break.",
    "One-Time Pad": (
        "*Perfect secrecy requires a truly random key, "
        "as long as the message, and never reused."
    ),
    "RSA": (
        "512-bit RSA is for learning only. "
        "Real RSA requires appropriate key sizes and secure padding."
    ),
    "Vigenère": (
        "k is the keyword length. Longer keywords mean more possible keys."
    ),
}

KEY_HINT = {
    "Caesar": "A whole number, e.g. 3",
    "Affine": "Two numbers a,b e.g. 5,8 (a must be coprime with 26)",
    "Vigenère": "A word, e.g. lemon",
    "XOR": "Any text",
    "One-Time Pad": "Hex key at least as long as the message",
    "AES": "A password",
    "ChaCha20": "A password",
}

TEXT_ALGOS = list(INFO)
FILE_ALGOS = ["AES", "ChaCha20"]


# ==================================================
# PAGE SETUP AND THEME
# ==================================================

def setup(title, icon):
    st.set_page_config(
        page_title=f"CryptoMath | {title}",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0b1020;
        }

        [data-testid="stSidebar"] {
            background-color: #111a2d;
            border-right: 1px solid #263451;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2 {
            color: #f4f3ff;
        }

        h1, h2, h3 {
            color: #f4f3ff;
        }

        p, li, label {
            color: #c4cbe0;
        }

        [data-testid="stMetric"] {
            background-color: #151f35;
            border: 1px solid #293858;
            padding: 16px;
            border-radius: 12px;
        }

        [data-testid="stMetricValue"] {
            color: #b9adff;
        }

        .stButton > button,
        .stDownloadButton > button {
            border-radius: 9px;
            border: 1px solid #6656bd;
        }

        div[data-testid="stTabs"] button {
            color: #c4cbe0;
        }

        hr {
            border-color: #293858;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar branding using native Streamlit components
    with st.sidebar:
        st.title("🔐 CryptoMath")
        st.caption("DISCRETE MATHEMATICS PROJECT")
        st.divider()
        st.caption("Explore cryptography, algorithms and mathematics.")

    # Main page title
    st.title(f"{icon} {title}")


# ==================================================
# INTEGER VALIDATION
# ==================================================

def _int(text, msg):
    try:
        return int(text)
    except (ValueError, TypeError):
        raise ValueError(msg) from None


# ==================================================
# TEXT ENCRYPTION AND DECRYPTION
# ==================================================

def run_text(algo, enc, text, key, rsa_keys=None):

    if algo == "Caesar":
        k = _int(
            key,
            "Caesar key must be a whole number, e.g. 3"
        )

        return (
            caesar.encrypt(text, k)
            if enc
            else caesar.decrypt(text, k)
        )

    if algo == "Affine":
        parts = key.split(",")

        if len(parts) != 2:
            raise ValueError("Affine key must look like 5,8")

        a, b = (
            _int(x.strip(), "Affine key must look like 5,8")
            for x in parts
        )

        return (
            affine.encrypt(text, a, b)
            if enc
            else affine.decrypt(text, a, b)
        )

    if algo == "Vigenère":
        return (
            vigenere.encrypt(text, key)
            if enc
            else vigenere.decrypt(text, key)
        )

    if algo == "XOR":
        if enc:
            return xor_cipher.xor_bytes(
                text.encode(),
                key.encode()
            ).hex()

        return xor_cipher.xor_bytes(
            bytes.fromhex(text),
            key.encode()
        ).decode()

    if algo == "One-Time Pad":
        return (
            otp.encrypt(text, key)
            if enc
            else otp.decrypt(text, key)
        )

    if algo == "RSA":
        if rsa_keys is None:
            raise ValueError("RSA keys are required.")

        if enc:
            return rsa.encrypt(
                text,
                rsa_keys["n"],
                rsa_keys["e"]
            )

        return rsa.decrypt(
            text,
            rsa_keys["n"],
            rsa_keys["d"]
        )

    if algo == "AES":
        mod = aes
    elif algo == "ChaCha20":
        mod = chacha
    else:
        raise ValueError("Unknown encryption algorithm.")

    if enc:
        encrypted = mod.encrypt(text.encode(), key)
        return base64.b64encode(encrypted).decode()

    decrypted = mod.decrypt(
        base64.b64decode(text),
        key
    )

    return decrypted.decode()


# ==================================================
# ENCRYPTION STATISTICS
# ==================================================

def show_stats(algo, dt, enc):

    size, level = INFO[algo]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Encryption time" if enc else "Decryption time",
        f"{dt * 1000:.2f} ms"
    )

    c2.metric(
        "Key size",
        size
    )

    c3.metric(
        "Security level",
        level
    )

    if NOTES.get(algo):
        st.caption(NOTES[algo])

import base64
import streamlit as st

import caesar
import affine
import vigenere
import xor_cipher
import otp
import rsa
import aes
import chacha


# ==================================================
# ALGORITHM INFORMATION
# ==================================================

INFO = {
    "Caesar": ("26 keys", "Very weak"),
    "Affine": ("312 keys", "Very weak"),
    "Vigenère": ("26^k keys", "Weak"),
    "XOR": ("8 × key bytes", "Weak"),
    "One-Time Pad": ("Message length", "Perfect*"),
    "RSA": ("512-bit", "Demo only"),
    "ChaCha20": ("256-bit", "Strong"),
    "AES": ("256-bit", "Strong"),
}

NOTES = {
    "XOR": "A short repeating key is easy to break.",
    "One-Time Pad": (
        "*Perfect secrecy requires a truly random key, "
        "as long as the message, and never reused."
    ),
    "RSA": (
        "512-bit RSA is for learning only. "
        "Real RSA requires appropriate key sizes and secure padding."
    ),
    "Vigenère": (
        "k is the keyword length. Longer keywords mean more possible keys."
    ),
}

KEY_HINT = {
    "Caesar": "A whole number, e.g. 3",
    "Affine": "Two numbers a,b e.g. 5,8 (a must be coprime with 26)",
    "Vigenère": "A word, e.g. lemon",
    "XOR": "Any text",
    "One-Time Pad": "Hex key at least as long as the message",
    "AES": "A password",
    "ChaCha20": "A password",
}

TEXT_ALGOS = list(INFO)
FILE_ALGOS = ["AES", "ChaCha20"]


# ==================================================
# PAGE SETUP AND THEME
# ==================================================

def setup(title, icon):
    st.set_page_config(
        page_title=f"CryptoMath | {title}",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0b1020;
        }

        [data-testid="stSidebar"] {
            background-color: #111a2d;
            border-right: 1px solid #263451;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2 {
            color: #f4f3ff;
        }

        h1, h2, h3 {
            color: #f4f3ff;
        }

        p, li, label {
            color: #c4cbe0;
        }

        [data-testid="stMetric"] {
            background-color: #151f35;
            border: 1px solid #293858;
            padding: 16px;
            border-radius: 12px;
        }

        [data-testid="stMetricValue"] {
            color: #b9adff;
        }

        .stButton > button,
        .stDownloadButton > button {
            border-radius: 9px;
            border: 1px solid #6656bd;
        }

        div[data-testid="stTabs"] button {
            color: #c4cbe0;
        }

        hr {
            border-color: #293858;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar branding using native Streamlit components
    with st.sidebar:
        st.title("🔐 CryptoMath")
        st.caption("DISCRETE MATHEMATICS PROJECT")
        st.divider()
        st.caption("Explore cryptography, algorithms and mathematics.")

    # Main page title
    st.title(f"{icon} {title}")


# ==================================================
# INTEGER VALIDATION
# ==================================================

def _int(text, msg):
    try:
        return int(text)
    except (ValueError, TypeError):
        raise ValueError(msg) from None


# ==================================================
# TEXT ENCRYPTION AND DECRYPTION
# ==================================================

def run_text(algo, enc, text, key, rsa_keys=None):

    if algo == "Caesar":
        k = _int(
            key,
            "Caesar key must be a whole number, e.g. 3"
        )

        return (
            caesar.encrypt(text, k)
            if enc
            else caesar.decrypt(text, k)
        )

    if algo == "Affine":
        parts = key.split(",")

        if len(parts) != 2:
            raise ValueError("Affine key must look like 5,8")

        a, b = (
            _int(x.strip(), "Affine key must look like 5,8")
            for x in parts
        )

        return (
            affine.encrypt(text, a, b)
            if enc
            else affine.decrypt(text, a, b)
        )

    if algo == "Vigenère":
        return (
            vigenere.encrypt(text, key)
            if enc
            else vigenere.decrypt(text, key)
        )

    if algo == "XOR":
        if enc:
            return xor_cipher.xor_bytes(
                text.encode(),
                key.encode()
            ).hex()

        return xor_cipher.xor_bytes(
            bytes.fromhex(text),
            key.encode()
        ).decode()

    if algo == "One-Time Pad":
        return (
            otp.encrypt(text, key)
            if enc
            else otp.decrypt(text, key)
        )

    if algo == "RSA":
        if rsa_keys is None:
            raise ValueError("RSA keys are required.")

        if enc:
            return rsa.encrypt(
                text,
                rsa_keys["n"],
                rsa_keys["e"]
            )

        return rsa.decrypt(
            text,
            rsa_keys["n"],
            rsa_keys["d"]
        )

    if algo == "AES":
        mod = aes
    elif algo == "ChaCha20":
        mod = chacha
    else:
        raise ValueError("Unknown encryption algorithm.")

    if enc:
        encrypted = mod.encrypt(text.encode(), key)
        return base64.b64encode(encrypted).decode()

    decrypted = mod.decrypt(
        base64.b64decode(text),
        key
    )

    return decrypted.decode()


# ==================================================
# ENCRYPTION STATISTICS
# ==================================================

def show_stats(algo, dt, enc):

    size, level = INFO[algo]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Encryption time" if enc else "Decryption time",
        f"{dt * 1000:.2f} ms"
    )

    c2.metric(
        "Key size",
        size
    )

    c3.metric(
        "Security level",
        level
    )

    if NOTES.get(algo):
        st.caption(NOTES[algo])

import base64
import streamlit as st

import caesar
import affine
import vigenere
import xor_cipher
import otp
import rsa
import aes
import chacha


# ==================================================
# ALGORITHM INFORMATION
# ==================================================

INFO = {
    "Caesar": ("26 keys", "Very weak"),
    "Affine": ("312 keys", "Very weak"),
    "Vigenère": ("26^k keys", "Weak"),
    "XOR": ("8 × key bytes", "Weak"),
    "One-Time Pad": ("Message length", "Perfect*"),
    "RSA": ("512-bit", "Demo only"),
    "ChaCha20": ("256-bit", "Strong"),
    "AES": ("256-bit", "Strong"),
}

NOTES = {
    "XOR": "A short repeating key is easy to break.",
    "One-Time Pad": (
        "*Perfect secrecy requires a truly random key, "
        "as long as the message, and never reused."
    ),
    "RSA": (
        "512-bit RSA is for learning only. "
        "Real RSA requires appropriate key sizes and secure padding."
    ),
    "Vigenère": (
        "k is the keyword length. Longer keywords mean more possible keys."
    ),
}

KEY_HINT = {
    "Caesar": "A whole number, e.g. 3",
    "Affine": "Two numbers a,b e.g. 5,8 (a must be coprime with 26)",
    "Vigenère": "A word, e.g. lemon",
    "XOR": "Any text",
    "One-Time Pad": "Hex key at least as long as the message",
    "AES": "A password",
    "ChaCha20": "A password",
}

TEXT_ALGOS = list(INFO)
FILE_ALGOS = ["AES", "ChaCha20"]


# ==================================================
# PAGE SETUP AND THEME
# ==================================================

def setup(title, icon):
    st.set_page_config(
        page_title=f"CryptoMath | {title}",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0b1020;
        }

        [data-testid="stSidebar"] {
            background-color: #111a2d;
            border-right: 1px solid #263451;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2 {
            color: #f4f3ff;
        }

        h1, h2, h3 {
            color: #f4f3ff;
        }

        p, li, label {
            color: #c4cbe0;
        }

        [data-testid="stMetric"] {
            background-color: #151f35;
            border: 1px solid #293858;
            padding: 16px;
            border-radius: 12px;
        }

        [data-testid="stMetricValue"] {
            color: #b9adff;
        }

        .stButton > button,
        .stDownloadButton > button {
            border-radius: 9px;
            border: 1px solid #6656bd;
        }

        div[data-testid="stTabs"] button {
            color: #c4cbe0;
        }

        hr {
            border-color: #293858;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar branding using native Streamlit components
    with st.sidebar:
        st.title("🔐 CryptoMath")
        st.caption("DISCRETE MATHEMATICS PROJECT")
        st.divider()
        st.caption("Explore cryptography, algorithms and mathematics.")

    # Main page title
    st.title(f"{icon} {title}")


# ==================================================
# INTEGER VALIDATION
# ==================================================

def _int(text, msg):
    try:
        return int(text)
    except (ValueError, TypeError):
        raise ValueError(msg) from None


# ==================================================
# TEXT ENCRYPTION AND DECRYPTION
# ==================================================

def run_text(algo, enc, text, key, rsa_keys=None):

    if algo == "Caesar":
        k = _int(
            key,
            "Caesar key must be a whole number, e.g. 3"
        )

        return (
            caesar.encrypt(text, k)
            if enc
            else caesar.decrypt(text, k)
        )

    if algo == "Affine":
        parts = key.split(",")

        if len(parts) != 2:
            raise ValueError("Affine key must look like 5,8")

        a, b = (
            _int(x.strip(), "Affine key must look like 5,8")
            for x in parts
        )

        return (
            affine.encrypt(text, a, b)
            if enc
            else affine.decrypt(text, a, b)
        )

    if algo == "Vigenère":
        return (
            vigenere.encrypt(text, key)
            if enc
            else vigenere.decrypt(text, key)
        )

    if algo == "XOR":
        if enc:
            return xor_cipher.xor_bytes(
                text.encode(),
                key.encode()
            ).hex()

        return xor_cipher.xor_bytes(
            bytes.fromhex(text),
            key.encode()
        ).decode()

    if algo == "One-Time Pad":
        return (
            otp.encrypt(text, key)
            if enc
            else otp.decrypt(text, key)
        )

    if algo == "RSA":
        if rsa_keys is None:
            raise ValueError("RSA keys are required.")

        if enc:
            return rsa.encrypt(
                text,
                rsa_keys["n"],
                rsa_keys["e"]
            )

        return rsa.decrypt(
            text,
            rsa_keys["n"],
            rsa_keys["d"]
        )

    if algo == "AES":
        mod = aes
    elif algo == "ChaCha20":
        mod = chacha
    else:
        raise ValueError("Unknown encryption algorithm.")

    if enc:
        encrypted = mod.encrypt(text.encode(), key)
        return base64.b64encode(encrypted).decode()

    decrypted = mod.decrypt(
        base64.b64decode(text),
        key
    )

    return decrypted.decode()


# ==================================================
# ENCRYPTION STATISTICS
# ==================================================

def show_stats(algo, dt, enc):

    size, level = INFO[algo]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Encryption time" if enc else "Decryption time",
        f"{dt * 1000:.2f} ms"
    )

    c2.metric(
        "Key size",
        size
    )

    c3.metric(
        "Security level",
        level
    )

    if NOTES.get(algo):
        st.caption(NOTES[algo])
