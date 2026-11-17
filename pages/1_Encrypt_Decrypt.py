
import time
import streamlit as st

import common
import otp
import rsa
import aes
import chacha
import strength
import hashing


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

common.setup("Encrypt & Decrypt", "🔐")

st.markdown("""
<div class="hero-panel">
    <div style="font-size:13px; color:#A99EFF; letter-spacing:2px;
                font-weight:700; margin-bottom:10px;">
        CRYPTOMATH / CRYPTOGRAPHY WORKSPACE
    </div>
    <h1 style="margin:0; font-size:36px;">
        Encrypt. Decrypt. <span style="color:#A99EFF;">Secure.</span>
    </h1>
    <p style="color:#AAB4CC; font-size:15px; margin-top:12px;">
        Experiment with cryptographic algorithms, protect your files,
        and understand how encryption works.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

# Quick information
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("**01 · TEXT ENCRYPTION**")
    st.caption("Convert readable messages into ciphertext.")

with c2:
    st.markdown("**02 · FILE ENCRYPTION**")
    st.caption("Protect files using AES or ChaCha20.")

with c3:
    st.markdown("**03 · KEY MANAGEMENT**")
    st.caption("Generate, load and manage encryption keys.")

st.divider()


# --------------------------------------------------
# TEXT ENCRYPTION
# --------------------------------------------------

tab_text, tab_file = st.tabs([
    "✉️  Text Encryption",
    "📁  File Encryption"
])


with tab_text:

    st.subheader("Text Encryption Workspace")
    st.caption("Choose an algorithm, enter your message and configure its key.")

    left, right = st.columns([1, 1])

    with left:
        algo = st.selectbox(
            "Select encryption algorithm",
            common.TEXT_ALGOS,
            key="text_algorithm"
        )

    with right:
        mode = st.radio(
            "Operation",
            ["Encrypt", "Decrypt"],
            horizontal=True,
            key="text_operation"
        )

    enc = mode == "Encrypt"

    st.markdown("---")

    text = st.text_area(
        "Your message",
        height=160,
        placeholder="Enter the text you want to encrypt or decrypt...",
        key="text_input_message"
    )

    key = ""
    rsa_keys = None

    # --------------------------------------------------
    # RSA KEY MANAGEMENT
    # --------------------------------------------------

    if algo == "RSA":

        st.markdown("#### RSA Key Management")
        st.info(
            "RSA uses a public key for encryption and a private key "
            "for decryption. Save your keys if you want to use them later."
        )

        if "rsa" not in st.session_state:
            st.session_state.rsa = rsa.generate_keys(512)

        with st.expander("Manage RSA keys", expanded=False):

            if st.button("Generate new RSA keys", key="new_rsa_keys"):
                st.session_state.rsa = rsa.generate_keys(512)
                st.success("New RSA keys generated.")

            uploaded_keys = st.file_uploader(
                "Import previously saved keys",
                type="json",
                key="rsa_up"
            )

            if uploaded_keys is not None:
                signature = (uploaded_keys.name, uploaded_keys.size)

                if st.session_state.get("rsa_sig") != signature:
                    try:
                        st.session_state.rsa = rsa.import_keys(
                            uploaded_keys.getvalue().decode(
                                errors="replace"
                            )
                        )
                        st.session_state.rsa_sig = signature
                        st.success("RSA keys imported successfully.")

                    except ValueError as err:
                        st.error(str(err))

            exported_keys = rsa.export_keys(st.session_state.rsa)

            st.download_button(
                "Download RSA keys",
                exported_keys,
                file_name="rsa_keys.json",
                mime="application/json",
                key="download_rsa_keys"
            )

            st.code(exported_keys, language="json")

        rsa_keys = st.session_state.rsa

    else:

        # --------------------------------------------------
        # NORMAL KEY INPUT
        # --------------------------------------------------

        st.markdown("#### Encryption Key")

        if algo == "One-Time Pad" and enc:

            if st.button(
                "Generate random key for this message",
                key="generate_otp_key",
                disabled=not text
            ):
                st.session_state["key_One-Time Pad"] = (
                    otp.generate_key(len(text.encode()))
                )

            if st.session_state.get("key_One-Time Pad"):
                st.success("Random key generated. Keep it safe!")
                st.code(st.session_state["key_One-Time Pad"])

        key = st.text_input(
            "Enter your key",
            key=f"key_{algo}",
            type="password" if algo in ("AES", "ChaCha20") else "default",
            help=common.KEY_HINT[algo],
            placeholder=common.KEY_HINT[algo]
        )

        if algo in ("AES", "ChaCha20") and enc and key:

            bits = strength.analyse(key)[1]

            st.progress(
                min(bits / 80, 1.0),
                text=(
                    f"Password strength: {strength.label(bits)} "
                    f"(approximately {bits:.0f} bits)"
                )
            )

        if algo in common.NOTES:
            st.caption(common.NOTES[algo])


    # --------------------------------------------------
    # ENCRYPT / DECRYPT ACTION
    # --------------------------------------------------

    st.markdown("---")

    button_label = "🔒 Encrypt Message" if enc else "🔓 Decrypt Message"

    if st.button(
        button_label,
        type="primary",
        use_container_width=True,
        key="run_text"
    ):

        if not text:
            st.warning("Please enter a message first.")

        elif algo != "RSA" and not key:
            st.warning("Please enter an encryption key.")

        else:
            try:
                start_time = time.perf_counter()

                output = common.run_text(
                    algo,
                    enc,
                    text,
                    key,
                    rsa_keys
                )

                elapsed = time.perf_counter() - start_time

                st.session_state.text_result = {
                    "output": output,
                    "time": elapsed,
                    "algorithm": algo,
                    "encrypted": enc
                }

            except UnicodeDecodeError:
                st.error(
                    "Decryption failed. The key may be incorrect, "
                    "or the data may not be valid."
                )

            except Exception as err:
                st.error(
                    f"Operation failed: {err}"
                    if str(err)
                    else "Operation failed. Check your key and input."
                )


    # --------------------------------------------------
    # DISPLAY TEXT RESULT
    # --------------------------------------------------

    result = st.session_state.get("text_result")

    if result:

        st.markdown("---")
        st.subheader("Operation Result")

        if result["encrypted"]:
            st.success("Message encrypted successfully.")
        else:
            st.success("Message decrypted successfully.")

        st.text_area(
            "Output",
            value=result["output"],
            height=160,
            key="display_text_result"
        )

        st.download_button(
            "Download result",
            data=result["output"],
            file_name=(
                "encrypted_message.txt"
                if result["encrypted"]
                else "decrypted_message.txt"
            ),
            mime="text/plain",
            use_container_width=True,
            key="download_text_result"
        )

        st.markdown("#### Performance Statistics")

        common.show_stats(
            result["algorithm"],
            result["time"],
            result["encrypted"]
        )


# --------------------------------------------------
# FILE ENCRYPTION
# --------------------------------------------------

with tab_file:

    st.subheader("File Encryption Workspace")

    st.caption(
        "Encrypt or decrypt files using AES or ChaCha20."
    )

    st.info(
        "Your original file is not modified. The result is provided "
        "as a separate downloadable file."
    )

    uploaded_file = st.file_uploader(
        "Upload your file",
        key="file_in"
    )

    if uploaded_file:

        st.markdown("#### Selected File")

        f1, f2 = st.columns(2)

        with f1:
            st.markdown(f"**Filename:** {uploaded_file.name}")

        with f2:
            st.markdown(
                f"**File size:** {uploaded_file.size:,} bytes"
            )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        algo2 = st.selectbox(
            "Encryption algorithm",
            common.FILE_ALGOS,
            key="file_algo"
        )

    with col2:
        mode2 = st.radio(
            "Operation",
            ["Encrypt", "Decrypt"],
            horizontal=True,
            key="file_mode"
        )

    enc2 = mode2 == "Encrypt"

    password = st.text_input(
        "Encryption password",
        type="password",
        key="file_pw",
        placeholder="Enter your password"
    )

    if password and enc2:

        bits = strength.analyse(password)[1]

        st.progress(
            min(bits / 80, 1.0),
            text=(
                f"Password strength: {strength.label(bits)} "
                f"(approximately {bits:.0f} bits)"
            )
        )

    st.markdown("---")

    file_button_label = (
        "🔒 Encrypt File" if enc2 else "🔓 Decrypt File"
    )

    if st.button(
        file_button_label,
        type="primary",
        use_container_width=True,
        key="run_file"
    ):

        if uploaded_file is None:
            st.warning("Please upload a file.")

        elif not password:
            st.warning("Please enter a password.")

        else:

            module = aes if algo2 == "AES" else chacha

            extension = (
                ".aes" if algo2 == "AES" else ".chacha"
            )

            try:

                file_data = uploaded_file.getvalue()

                start_time = time.perf_counter()

                output = (
                    module.encrypt(file_data, password)
                    if enc2
                    else module.decrypt(file_data, password)
                )

                elapsed = time.perf_counter() - start_time

                if enc2:
                    output_name = uploaded_file.name + extension

                else:
                    if uploaded_file.name.endswith(extension):
                        output_name = uploaded_file.name[:-len(extension)]
                    else:
                        output_name = "decrypted_" + uploaded_file.name

                original_data = output if not enc2 else file_data

                st.session_state.file_result = {
                    "name": output_name,
                    "output": output,
                    "time": elapsed,
                    "encrypted": enc2,
                    "algorithm": algo2,
                    "sha": hashing.sha256_hex(original_data)
                }

            except Exception:
                st.session_state.pop("file_result", None)

                st.error(
                    "File operation failed. Check the password, "
                    "algorithm and file integrity."
                )


    # --------------------------------------------------
    # FILE RESULT
    # --------------------------------------------------

    file_result = st.session_state.get("file_result")

    if file_result:

        st.markdown("---")
        st.subheader("File Operation Result")

        st.success(
            f"Completed successfully: {file_result['name']}"
        )

        r1, r2 = st.columns(2)

        with r1:
            st.metric(
                "Algorithm",
                file_result["algorithm"]
            )

        with r2:
            st.metric(
                "Processing time",
                f"{file_result['time'] * 1000:.2f} ms"
            )

        st.markdown("#### File Integrity")

        st.caption(
            "SHA-256 hash of the original readable file:"
        )

        st.code(file_result["sha"])

        st.download_button(
            "⬇️ Download processed file",
            data=file_result["output"],
            file_name=file_result["name"],
            use_container_width=True,
            key="file_dl"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:15px 0;">
    <div style="font-size:13px; color:#A99EFF; font-weight:700;">
        CRYPTOMATH
    </div>
    <div style="font-size:12px; color:#8792AA; margin-top:5px;">
        Understanding the mathematics behind cryptography.
    </div>
</div>
""", unsafe_allow_html=True)
