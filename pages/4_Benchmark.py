
import time
import pandas as pd
import streamlit as st

import common
import otp
import rsa


# PAGE SETUP
common.setup("Benchmark", "⚡")

st.title("Performance Benchmark")
st.caption("Compare the performance of cryptographic algorithms.")

st.divider()

st.subheader("Benchmark Configuration")

message_size = st.slider(
    "Message size (characters)",
    min_value=100,
    max_value=2000,
    value=500,
    step=100
)

st.info(
    "The benchmark uses the same sample message for each algorithm. "
    "Results depend on your computer and are not universal performance ratings."
)

st.markdown("#### Algorithms included")

st.write(", ".join(common.TEXT_ALGOS))

st.divider()

if st.button(
    "Run Benchmark",
    type="primary",
    use_container_width=True
):
    message = (
        "The quick brown fox jumps over the lazy dog. "
        * (message_size // 45 + 1)
    )[:message_size]

    results = []

    try:
        with st.spinner("Generating RSA keys and running benchmarks..."):

            # RSA KEY GENERATION
            start = time.perf_counter()
            rsa_keys = rsa.generate_keys(512)
            rsa_keygen_time = (time.perf_counter() - start) * 1000

            # KEYS FOR EACH ALGORITHM
            keys = {
                "Caesar": "3",
                "Affine": "5,8",
                "Vigenère": "lemon",
                "XOR": "key",
                "One-Time Pad": otp.generate_key(len(message.encode())),
                "RSA": "",
                "ChaCha20": "benchmark-password",
                "AES": "benchmark-password"
            }

            # BENCHMARK EACH ALGORITHM
            for algorithm in common.TEXT_ALGOS:

                key = keys[algorithm]

                # ENCRYPTION
                start = time.perf_counter()

                encrypted = common.run_text(
                    algorithm,
                    True,
                    message,
                    key,
                    rsa_keys
                )

                encryption_time = (
                    time.perf_counter() - start
                ) * 1000

                # DECRYPTION
                start = time.perf_counter()

                decrypted = common.run_text(
                    algorithm,
                    False,
                    encrypted,
                    key,
                    rsa_keys
                )

                decryption_time = (
                    time.perf_counter() - start
                ) * 1000

                # VERIFY RESULT
                verified = decrypted == message

                results.append({
                    "Algorithm": algorithm,
                    "Encryption (ms)": round(encryption_time, 3),
                    "Decryption (ms)": round(decryption_time, 3),
                    "Key Size": common.INFO[algorithm][0],
                    "Security": common.INFO[algorithm][1],
                    "Verified": "Yes" if verified else "No"
                })

        st.session_state["benchmark_results"] = results
        st.session_state["rsa_keygen_time"] = rsa_keygen_time
        st.session_state["benchmark_size"] = message_size

    except Exception as error:
        st.error("Benchmark could not be completed: " + str(error))


# DISPLAY RESULTS
results = st.session_state.get("benchmark_results")

if results:
    st.divider()
    st.subheader("Benchmark Results")

    st.metric(
        "RSA key generation",
        f"{st.session_state['rsa_keygen_time']:.2f} ms"
    )

    st.metric(
        "Message size",
        f"{st.session_state['benchmark_size']:,} characters"
    )

    df = pd.DataFrame(results)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("#### Encryption and Decryption Comparison")

    chart_df = df.set_index("Algorithm")[
        ["Encryption (ms)", "Decryption (ms)"]
    ]

    st.bar_chart(
        chart_df,
        use_container_width=True
    )

    st.markdown("#### Fastest Algorithms")

    fastest_encryption = min(
        results,
        key=lambda item: item["Encryption (ms)"]
    )

    fastest_decryption = min(
        results,
        key=lambda item: item["Decryption (ms)"]
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Fastest encryption",
            fastest_encryption["Algorithm"],
            f"{fastest_encryption['Encryption (ms)']} ms"
        )

    with c2:
        st.metric(
            "Fastest decryption",
            fastest_decryption["Algorithm"],
            f"{fastest_decryption['Decryption (ms)']} ms"
        )

    if all(item["Verified"] == "Yes" for item in results):
        st.success("All algorithms successfully recovered the original message.")
    else:
        st.warning("One or more algorithms did not recover the original message.")

    st.caption(
        "RSA uses a 512-bit key here for educational demonstration only. "
        "AES and ChaCha20 timings include password-based key derivation."
    )

    csv = df.to_csv(index=False)

    st.download_button(
        "Download Benchmark Results (CSV)",
        data=csv,
        file_name="cryptomath_benchmark.csv",
        mime="text/csv",
        use_container_width=True
    )


# FOOTER
st.divider()
st.caption("CRYPTOMATH | PERFORMANCE BENCHMARK")
