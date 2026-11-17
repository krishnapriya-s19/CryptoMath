
import streamlit as st

import common
import hashing


# PAGE SETUP
common.setup("Hash and Integrity", "🧾")

st.title("Hash & Integrity Lab")
st.caption(
    "Verify file integrity and explore the properties of cryptographic hashes."
)

st.divider()

tab1, tab2, tab3 = st.tabs([
    "Hash a File",
    "Compare Files",
    "Avalanche Effect"
])


# ==================================================
# TAB 1 - HASH A FILE
# ==================================================

with tab1:
    st.subheader("SHA-256 File Hashing")

    st.write(
        "Upload a file to generate its SHA-256 hash. "
        "You can compare the result with an expected hash."
    )

    uploaded_file = st.file_uploader(
        "Choose a file",
        key="hash_file"
    )

    if uploaded_file is not None:
        file_data = uploaded_file.getvalue()
        file_hash = hashing.sha256_hex(file_data)

        st.divider()

        c1, c2 = st.columns(2)

        with c1:
            st.metric("File name", uploaded_file.name)

        with c2:
            st.metric("File size", f"{len(file_data):,} bytes")

        st.markdown("#### Generated SHA-256 Hash")

        st.code(file_hash)

        st.download_button(
            "Download SHA-256 Hash",
            data=file_hash,
            file_name=uploaded_file.name + ".sha256",
            mime="text/plain",
            use_container_width=True
        )

        st.markdown("#### Verify File Integrity")

        expected_hash = st.text_input(
            "Enter expected SHA-256 hash",
            placeholder="Paste the expected 64-character hash...",
            key="expected_hash"
        ).strip().lower()

        if expected_hash:
            if expected_hash == file_hash:
                st.success("Hash match. The file matches the expected hash.")
            else:
                st.error("Hash mismatch. The file does not match the expected hash.")

        st.caption(
            "Tip: Hash a file before and after an encryption/decryption "
            "round trip. Matching hashes indicate that the file contents "
            "are identical."
        )


# ==================================================
# TAB 2 - COMPARE TWO FILES
# ==================================================

with tab2:
    st.subheader("File Comparison")

    st.write(
        "Upload two files to compare their SHA-256 hashes."
    )

    c1, c2 = st.columns(2)

    with c1:
        file_a = st.file_uploader(
            "Upload first file",
            key="compare_file_a"
        )

    with c2:
        file_b = st.file_uploader(
            "Upload second file",
            key="compare_file_b"
        )

    if file_a is not None and file_b is not None:
        data_a = file_a.getvalue()
        data_b = file_b.getvalue()

        hash_a = hashing.sha256_hex(data_a)
        hash_b = hashing.sha256_hex(data_b)

        st.divider()

        st.markdown("#### First File")

        st.write("Filename: " + file_a.name)
        st.code(hash_a)

        st.markdown("#### Second File")

        st.write("Filename: " + file_b.name)
        st.code(hash_b)

        st.markdown("#### Comparison Result")

        if hash_a == hash_b:
            st.success(
                "The SHA-256 hashes match. The file contents are identical."
            )
        else:
            st.error(
                "The SHA-256 hashes do not match. The file contents differ."
            )

        st.caption(
            "This comparison checks file contents, not filenames. "
            "Two files with different names can still have identical contents."
        )

    elif file_a is not None or file_b is not None:
        st.info("Upload both files to compare them.")


# ==================================================
# TAB 3 - AVALANCHE EFFECT
# ==================================================

with tab3:
    st.subheader("Avalanche Effect Demonstration")

    st.write(
        "The avalanche effect means that a small change in the input "
        "should produce a significantly different hash output."
    )

    st.info(
        "Change just one character in Text B and observe how many "
        "bits differ between the two SHA-256 hashes."
    )

    text_a = st.text_input(
        "Text A",
        value="hello world",
        key="avalanche_a"
    )

    text_b = st.text_input(
        "Text B",
        value="hello worle",
        key="avalanche_b"
    )

    if text_a == text_b:
        st.warning("Enter two different text values to compare them.")

    else:
        hash_a = hashing.sha256_hex(text_a.encode("utf-8"))
        hash_b = hashing.sha256_hex(text_b.encode("utf-8"))

        different_bits = hashing.avalanche(text_a, text_b)

        st.divider()

        st.markdown("#### Hash A")

        st.code(hash_a)

        st.markdown("#### Hash B")

        st.code(hash_b)

        st.markdown("#### Avalanche Result")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Different bits",
                f"{different_bits} / 256"
            )

        with c2:
            percentage = (different_bits / 256) * 100

            st.metric(
                "Percentage changed",
                f"{percentage:.2f}%"
            )

        st.progress(different_bits / 256)

        st.caption(
            "For a well-designed cryptographic hash, changing a small "
            "part of the input typically changes about half of the "
            "output bits."
        )

        st.markdown("#### Why is this important?")

        st.write(
            "The avalanche effect makes it difficult to predict how "
            "a small input change will affect the resulting hash. "
            "It is an important design property of cryptographic hash functions."
        )


# FOOTER
st.divider()
st.caption("CRYPTOMATH | HASH & INTEGRITY LAB")
