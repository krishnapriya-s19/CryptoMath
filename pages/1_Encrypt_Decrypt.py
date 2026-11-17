import time
import streamlit as st
import common, otp, rsa, aes, chacha, strength, hashing

common.setup("Encrypt & Decrypt", "🔐")
tab_text, tab_file = st.tabs(["Text", "File"])

with tab_text:
    algo = st.selectbox("Algorithm", common.TEXT_ALGOS)
    mode = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True)
    enc = mode == "Encrypt"
    text = st.text_area("Input", height=120)
    key, rsa_keys = "", None

    if algo == "RSA":
        if "rsa" not in st.session_state:
            st.session_state.rsa = rsa.generate_keys(512)
        with st.expander("RSA keys (download them to decrypt later)"):
            if st.button("Generate new keys"):
                st.session_state.rsa = rsa.generate_keys(512)
            up = st.file_uploader("Load saved keys (.json)", type="json", key="rsa_up")
            if up is not None and st.session_state.get("rsa_sig") != (up.name, up.size):
                try:
                    st.session_state.rsa = rsa.import_keys(up.getvalue().decode(errors="replace"))
                    st.session_state.rsa_sig = (up.name, up.size)
                    st.success("Keys loaded")
                except ValueError as err:
                    st.error(str(err))
            st.download_button("Download keys", rsa.export_keys(st.session_state.rsa), file_name="rsa_keys.json")
            st.code(rsa.export_keys(st.session_state.rsa), language="json")
        rsa_keys = st.session_state.rsa
    else:
        if algo == "One-Time Pad" and enc and st.button("Generate random key for this message"):
            st.session_state["key_One-Time Pad"] = otp.generate_key(len(text.encode()))
        key = st.text_input("Key", key=f"key_{algo}",
                            type="password" if algo in ("AES", "ChaCha20") else "default",
                            help=common.KEY_HINT[algo])
        if algo in ("AES", "ChaCha20") and enc and key:
            bits = strength.analyse(key)[1]
            st.progress(min(bits / 80, 1.0), text=f"Password strength: {strength.label(bits)} (~{bits:.0f} bits)")

    if st.button("Run", type="primary", key="run_text"):
        try:
            t0 = time.perf_counter()
            out = common.run_text(algo, enc, text, key, rsa_keys)
            dt = time.perf_counter() - t0
            st.text_area("Result (copy from here)", out, height=140)
            common.show_stats(algo, dt, enc)
        except UnicodeDecodeError:
            st.error("Failed: wrong key (the output is not readable text).")
        except Exception as err:
            st.error(f"Failed: {err}" if str(err) else "Failed: wrong key or tampered data.")

with tab_file:
    f = st.file_uploader("Choose a file", key="file_in")
    algo2 = st.selectbox("Algorithm", common.FILE_ALGOS, key="file_algo")
    mode2 = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True, key="file_mode")
    enc2 = mode2 == "Encrypt"
    pw = st.text_input("Password", type="password", key="file_pw")
    if pw and enc2:
        bits = strength.analyse(pw)[1]
        st.progress(min(bits / 80, 1.0), text=f"Password strength: {strength.label(bits)} (~{bits:.0f} bits)")

    if f and pw and st.button("Run", type="primary", key="run_file"):
        mod = aes if algo2 == "AES" else chacha
        ext = ".aes" if algo2 == "AES" else ".chacha"
        try:
            data = f.getvalue()
            t0 = time.perf_counter()
            out = mod.encrypt(data, pw) if enc2 else mod.decrypt(data, pw)
            dt = time.perf_counter() - t0
            if enc2:
                name = f.name + ext
            else:
                name = f.name[:-len(ext)] if f.name.endswith(ext) else "decrypted_" + f.name
            st.session_state.file_result = dict(name=name, out=out, dt=dt, enc=enc2, algo=algo2,
                                                sha=hashing.sha256_hex(data if enc2 else out))
        except Exception:
            st.session_state.pop("file_result", None)
            st.error("Failed: wrong password, wrong algorithm, or corrupted file.")

    r = st.session_state.get("file_result")
    if r:
        st.success(f"Done: {r['name']}")
        common.show_stats(r["algo"], r["dt"], r["enc"])
        st.caption(f"SHA-256 of the original (readable) file: {r['sha']}")
        st.download_button("Download result", r["out"], file_name=r["name"], key="file_dl")