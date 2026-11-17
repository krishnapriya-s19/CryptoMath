
import itertools
import math
import streamlit as st

import common
import number_theory as nt
import affine
import hashing


# ==================================================
# PAGE CONFIGURATION
# ==================================================

common.setup("Math Lab", "📐")

st.markdown("""
<div class="hero-panel">
    <div style="font-size:13px; color:#A99EFF; letter-spacing:2px;
                font-weight:700; margin-bottom:10px;">
        CRYPTOMATH / MATHEMATICAL EXPLORER
    </div>
    <h1 style="margin:0; font-size:36px;">
        The Mathematics <span style="color:#A99EFF;">Behind Security.</span>
    </h1>
    <p style="color:#AAB4CC; font-size:15px; margin-top:12px;">
        Explore the discrete mathematics, number theory and logic
        that make cryptographic algorithms work.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

# Overview cards
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("**01 · NUMBER THEORY**")
    st.caption("Prime numbers, GCD and modular arithmetic.")

with c2:
    st.markdown("**02 · COMBINATORICS**")
    st.caption("Key spaces, permutations and counting.")

with c3:
    st.markdown("**03 · LOGIC & SETS**")
    st.caption("Boolean logic and equivalence relations.")

st.divider()


# ==================================================
# HELPER FUNCTION
# ==================================================

def prime_factors(n):
    """Return the distinct prime factors of n."""
    fs = []
    p = 2

    while p * p <= n:
        if n % p == 0:
            fs.append(p)

            while n % p == 0:
                n //= p

        p += 1

    if n > 1:
        fs.append(n)

    return fs


def derangement(n):
    """Calculate the number of derangements using recurrence."""
    if n == 0:
        return 1

    if n == 1:
        return 0

    previous_previous = 1
    previous = 0

    for i in range(2, n + 1):
        current = (i - 1) * (
            previous + previous_previous
        )

        previous_previous = previous
        previous = current

    return previous


# ==================================================
# NAVIGATION TABS
# ==================================================

t1, t2, t3, t4, t5 = st.tabs([
    "🔤 Caesar",
    "🔁 Affine & Functions",
    "🔑 RSA Steps",
    "🔢 Counting & Sets",
    "🧠 Logic & Relations"
])


# ==================================================
# TAB 1: CAESAR CIPHER
# ==================================================

with t1:

    st.markdown("### Caesar Cipher")
    st.caption(
        "Understand how modular arithmetic shifts letters "
        "to produce ciphertext."
    )

    st.latex(
        r"C = (P + k) \bmod 26"
        r"\qquad"
        r"P = (C - k) \bmod 26"
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        word = st.text_input(
            "Enter a word",
            "HELLO",
            key="c_word"
        )

    with col2:
        k = st.slider(
            "Shift key (k)",
            1,
            25,
            3,
            key="c_shift"
        )

    rows = []

    for ch in word:

        if ch.isascii() and ch.isalpha():

            x = ord(ch.upper()) - 65
            y = (x + k) % 26

            rows.append({
                "Original letter": ch.upper(),
                "P": x,
                "P + k": x + k,
                "(P + k) mod 26": y,
                "Cipher letter": chr(y + 65)
            })

    if rows:

        st.markdown("---")
        st.markdown("#### Step-by-step transformation")

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True
        )

        ciphertext = "".join(
            r["Cipher letter"] for r in rows
        )

        st.markdown("#### Encrypted output")

        st.code(ciphertext, language="text")

        st.success(
            f"Successfully shifted {len(rows)} letters "
            f"using key k = {k}."
        )

        st.caption(
            "When P + k passes 25, mod 26 wraps it back "
            "to the beginning of the alphabet."
        )

    else:
        st.info("Enter at least one English alphabet letter.")


# ==================================================
# TAB 2: AFFINE CIPHER AND FUNCTIONS
# ==================================================

with t2:

    st.markdown("### Affine Cipher & Bijective Functions")

    st.caption(
        "Explore how coprime numbers determine whether "
        "an encryption function can be reversed."
    )

    st.latex(
        r"E(x) = (ax + b) \bmod 26"
        r"\qquad"
        r"D(y) = a^{-1}(y-b) \bmod 26"
    )

    col1, col2 = st.columns(2)

    with col1:
        a = st.selectbox(
            "Choose value of a",
            list(range(1, 26)),
            index=4,
            key="affine_a"
        )

    with col2:
        b = st.slider(
            "Choose value of b",
            0,
            25,
            8,
            key="affine_b"
        )

    g = nt.gcd(a, 26)

    distinct = len({
        (a * x + b) % 26
        for x in range(26)
    })

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    c1.metric("GCD (a, 26)", g)
    c2.metric("Distinct outputs", f"{distinct}/26")
    c3.metric(
        "Bijective?",
        "Yes" if distinct == 26 else "No"
    )

    if g == 1:

        inverse = nt.mod_inverse(a, 26)

        st.success(
            f"a = {a} is coprime with 26. "
            "Every letter maps to a different letter, "
            "so decryption is possible."
        )

        st.markdown("#### Modular inverse")

        st.latex(
            rf"a^{{-1}} = {inverse}"
            rf"\qquad"
            rf"({a} \times {inverse}) \bmod 26 = 1"
        )

        w = st.text_input(
            "Enter a word",
            "AFFINE",
            key="a_word"
        )

        if w:
            encrypted = affine.encrypt(w, a, b)

            st.markdown("#### Encrypted output")
            st.code(encrypted, language="text")

    else:

        st.error(
            f"gcd({a}, 26) = {g}, not 1. "
            "Some letters collide, so the function is "
            "not one-to-one and cannot be decrypted."
        )

    st.markdown("---")

    st.markdown("#### Valid Affine keys")

    st.write(
        f"Valid values of a: {affine.VALID_A}"
    )

    st.info(
        f"There are {len(affine.VALID_A)} valid values "
        f"of a = φ(26). Therefore, the total key space is "
        f"{len(affine.VALID_A)} × 26 = "
        f"**{len(affine.VALID_A) * 26} possible keys.**"
    )


# ==================================================
# TAB 3: RSA MATHEMATICAL STEPS
# ==================================================

with t3:

    st.markdown("### RSA Mathematical Explorer")

    st.caption(
        "Follow the mathematical process behind RSA "
        "using small example primes."
    )

    st.info(
        "This is a simplified educational demonstration. "
        "The small numbers used here are not suitable "
        "for real-world security."
    )

    st.latex(
        r"n = p \times q"
        r"\qquad"
        r"\phi(n) = (p-1)(q-1)"
    )

    st.latex(
        r"d = e^{-1} \bmod \phi(n)"
    )

    st.markdown("#### Input parameters")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        p = st.number_input(
            "Prime p",
            min_value=2,
            value=61,
            step=1,
            key="rsa_p"
        )

    with c2:
        q = st.number_input(
            "Prime q",
            min_value=2,
            value=53,
            step=1,
            key="rsa_q"
        )

    with c3:
        e = st.number_input(
            "Public exponent e",
            min_value=2,
            value=17,
            step=1,
            key="rsa_e"
        )

    with c4:
        m = st.number_input(
            "Message m",
            min_value=0,
            value=65,
            step=1,
            key="rsa_m"
        )

    st.markdown("---")

    if p == q or not (
        nt.is_prime(p) and nt.is_prime(q)
    ):

        st.warning(
            "p and q must be two different prime numbers."
        )

    else:

        n = p * q
        phi = (p - 1) * (q - 1)

        st.markdown("#### Step 1 · Calculate n")

        st.latex(
            rf"n = p \times q = {p} \times {q}"
            rf" = \boxed{{{n}}}"
        )

        st.markdown("#### Step 2 · Calculate Euler's totient")

        st.latex(
            rf"\phi(n) = (p-1)(q-1)"
            rf" = {p-1} \times {q-1}"
            rf" = \boxed{{{phi}}}"
        )

        g = nt.gcd(e, phi)

        if g != 1 or e >= phi:

            st.warning(
                f"Step 3: e must satisfy 1 < e < φ(n) "
                f"and gcd(e, φ(n)) = 1. "
                f"Here gcd({e}, {phi}) = {g}."
            )

        elif m >= n:

            st.warning(
                f"The message m must be smaller than n = {n}."
            )

        else:

            d = nt.mod_inverse(e, phi)

            c = nt.mod_exp(m, e, n)

            back = nt.mod_exp(c, d, n)

            st.markdown("#### Step 3 · Validate e")

            st.success(
                f"gcd({e}, {phi}) = 1. "
                "The selected public exponent is valid."
            )

            st.markdown("#### Step 4 · Calculate private exponent")

            st.latex(
                rf"d = e^{{-1}} \bmod \phi(n)"
                rf" = \boxed{{{d}}}"
            )

            st.caption(
                f"Check: {e} × {d} = "
                f"{e*d} ≡ {(e*d) % phi} mod {phi}"
            )

            st.markdown("#### Generated keys")

            k1, k2 = st.columns(2)

            with k1:
                st.markdown("**Public key**")
                st.code(f"({n}, {e})")

            with k2:
                st.markdown("**Private key**")
                st.code(f"({n}, {d})")

            st.markdown("---")

            st.markdown("#### Step 5 · Encryption")

            st.latex(
                rf"c = m^e \bmod n"
                rf" = {m}^{{{e}}} \bmod {n}"
                rf" = \boxed{{{c}}}"
            )

            st.markdown("#### Step 6 · Decryption")

            st.latex(
                rf"m = c^d \bmod n"
                rf" = {c}^{{{d}}} \bmod {n}"
                rf" = \boxed{{{back}}}"
            )

            if back == m:

                st.success(
                    "Verification successful! "
                    "The decrypted value matches the original message."
                )


# ==================================================
# TAB 4: COUNTING AND SETS
# ==================================================

with t4:

    st.markdown("### Counting, Combinatorics & Sets")

    st.caption(
        "Understand how mathematical counting determines "
        "the number of possible cryptographic keys."
    )

    # KEY SPACES

    st.markdown("#### 1. Cryptographic key spaces")

    spaces = {
        "Caesar": 26,
        "Affine": 12 * 26,
        "Vigenère (4-letter keyword)": 26 ** 4,
        "Substitution cipher": math.factorial(26),
        "AES-256": 2 ** 256
    }

    data = []

    for name, value in spaces.items():

        data.append({
            "Algorithm": name,
            "Number of keys": (
                f"{value:,}"
                if value < 10 ** 12
                else f"{value:.3e}"
            ),
            "Key space (bits)": round(
                math.log2(value), 1
            )
        })

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "A larger key space generally means more possible "
        "keys to consider, although security also depends "
        "on the algorithm and its implementation."
    )

    st.markdown("---")

    # PERMUTATIONS AND COMBINATIONS

    st.markdown("#### 2. Permutations and combinations")

    kk = st.slider(
        "Select keyword length",
        1,
        10,
        4,
        key="keyword_length"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Repeated letters allowed",
            f"{26 ** kk:,}"
        )
        st.latex(r"26^k")

    with c2:
        st.metric(
            "All different letters",
            f"{math.perm(26, kk):,}"
        )
        st.latex(r"P(26,k)")

    with c3:
        st.metric(
            "Order ignored",
            f"{math.comb(26, kk):,}"
        )
        st.latex(r"C(26,k)")

    st.markdown("---")

    # DERANGEMENTS

    st.markdown("#### 3. Derangements")

    st.caption(
        "A derangement is a permutation in which no element "
        "appears in its original position."
    )

    nn = st.slider(
        "Alphabet size",
        2,
        26,
        26,
        key="derangement_n"
    )

    D = derangement(nn)
    total_permutations = math.factorial(nn)

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            f"Derangements D({nn})",
            f"{D:,}"
        )

    with c2:
        st.metric(
            "Total permutations",
            f"{total_permutations:,}"
        )

    st.write(
        f"Fraction of derangements: "
        f"**{D / total_permutations:.4f}**"
    )

    st.caption(
        "As the alphabet size increases, the fraction "
        "approaches 1/e."
    )

    st.markdown("---")

    # SETS AND EULER PHI

    st.markdown("#### 4. Sets and Euler's phi function")

    st.caption(
        "Find the numbers between 1 and n that are coprime to n."
    )

    n = int(
        st.number_input(
            "Choose n",
            min_value=2,
            max_value=5000,
            value=26,
            step=1,
            key="phi_n"
        )
    )

    U = [
        x for x in range(1, n)
        if nt.gcd(x, n) == 1
    ]

    if n <= 60:

        st.markdown("**Set of units modulo n**")

        st.code(
            "U = {" + ", ".join(map(str, U)) + "}"
        )

    st.metric(
        "Number of coprime values |U|",
        len(U)
    )

    fs = prime_factors(n)

    terms = []
    total = 0

    for r in range(len(fs) + 1):

        for combo in itertools.combinations(fs, r):

            term = (
                (-1) ** r
                * (n // math.prod(combo))
            )

            total += term

            terms.append(
                ("+ " if term >= 0 else "− ")
                + str(abs(term))
            )

    st.markdown("**Prime factorisation**")

    st.write(f"Distinct prime factors: {fs}")

    st.markdown("**Inclusion-exclusion calculation**")

    st.latex(
        r"\phi(n) = n \prod_{p \mid n}"
        r"\left(1-\frac{1}{p}\right)"
    )

    st.write(
        " + ".join(terms).replace("+ −", "− ")
        + f" = **{total}**"
    )

    st.success(
        f"φ({n}) = {nt.totient(n)}. "
        f"This matches the number of elements in U."
    )


# ==================================================
# TAB 5: LOGIC AND RELATIONS
# ==================================================

with t5:

    st.markdown("### Logic, Relations & Hashing")

    st.caption(
        "Explore Boolean logic, equivalence relations "
        "and the pigeonhole principle."
    )

    # XOR TRUTH TABLE

    st.markdown("#### 1. XOR truth table")

    st.latex(
        r"P \oplus Q = "
        r"(P \lor Q) \land \neg(P \land Q)"
    )

    rows = []

    for P, Q in itertools.product([0, 1], repeat=2):

        rows.append({
            "P": P,
            "Q": Q,
            "P XOR Q": P ^ Q,
            "(P OR Q) AND NOT (P AND Q)": int(
                bool((P or Q) and not (P and Q))
            ),
            "(P XOR Q) XOR Q": (P ^ Q) ^ Q
        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )

    st.success(
        "The XOR expression matches the equivalent "
        "Boolean expression. XOR-ing twice with the same "
        "value restores the original value."
    )

    st.caption(
        "This is the mathematical property behind XOR-based "
        "encryption demonstrations."
    )

    st.markdown("---")

    # EQUIVALENCE RELATIONS

    st.markdown("#### 2. Congruence modulo n")

    st.caption(
        "Congruence modulo n is an equivalence relation."
    )

    mod = st.slider(
        "Select modulus n",
        2,
        12,
        5,
        key="relation_mod"
    )

    S = range(15)

    R = {
        (x, y)
        for x in S
        for y in S
        if (x - y) % mod == 0
    }

    refl = all(
        (x, x) in R
        for x in S
    )

    sym = all(
        (y, x) in R
        for (x, y) in R
    )

    trans = all(
        (x, z) in R
        for (x, y) in R
        for (y2, z) in R
        if y == y2
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Reflexive",
        "✓ Yes" if refl else "✗ No"
    )

    c2.metric(
        "Symmetric",
        "✓ Yes" if sym else "✗ No"
    )

    c3.metric(
        "Transitive",
        "✓ Yes" if trans else "✗ No"
    )

    st.markdown("**Equivalence classes**")

    for r in range(mod):

        equivalence_class = [
            x for x in S
            if x % mod == r
        ]

        st.write(
            f"**[{r}]** = "
            + "{"
            + ", ".join(map(str, equivalence_class))
            + "}"
        )

    st.success(
        f"The set is divided into {mod} equivalence classes."
    )

    st.caption(
        "Modular arithmetic is an important mathematical "
        "foundation of Caesar, Affine and RSA."
    )

    st.markdown("---")

    # PIGEONHOLE PRINCIPLE

    st.markdown("#### 3. Pigeonhole principle — Hash collisions")

    st.caption(
        "A hash function maps inputs to fixed-length outputs. "
        "A limited output space means collisions are possible."
    )

    st.info(
        "For this demonstration, SHA-256 outputs are shortened "
        "to 8 bits. This leaves only 256 possible outputs."
    )

    st.write(
        "By the pigeonhole principle, among 257 inputs, "
        "at least two must share the same 8-bit output."
    )

    seen = {}
    collision_found = False

    for i in range(257):

        h = hashing.sha256_hex(
            f"message {i}".encode()
        )[:2]

        if h in seen:

            st.success(
                f"Collision found: message {seen[h]} "
                f"and message {i} both produce {h}."
            )

            collision_found = True
            break

        seen[h] = i

    if not collision_found:

        st.warning(
            "No collision was found in this run."
        )

    st.caption(
        "This demonstration uses a deliberately shortened hash. "
        "It does not represent the security of the full SHA-256 hash."
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:15px 0;">
    <div style="font-size:13px; color:#A99EFF; font-weight:700;">
        CRYPTOMATH / MATH LAB
    </div>
    <div style="font-size:12px; color:#8792AA; margin-top:5px;">
        Mathematics is the foundation of cryptography.
    </div>
</div>
""", unsafe_allow_html=True)
