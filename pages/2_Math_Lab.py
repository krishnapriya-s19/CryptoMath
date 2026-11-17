import itertools
import math
import streamlit as st
import common, number_theory as nt, affine, hashing

common.setup("Math Lab", "📐")
st.caption("See the discrete mathematics behind each cipher, step by step.")

def prime_factors(n):
    fs, p = [], 2
    while p * p <= n:
        if n % p == 0:
            fs.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        fs.append(n)
    return fs

t1, t2, t3, t4, t5 = st.tabs(["Caesar", "Affine and functions", "RSA steps", "Counting and sets", "Logic and relations"])

with t1:
    word = st.text_input("Word", "HELLO", key="c_word")
    k = st.slider("Key k", 1, 25, 3)
    st.latex(r"C = (P + k) \bmod 26 \qquad P = (C - k) \bmod 26")
    rows = []
    for ch in word:
        if ch.isascii() and ch.isalpha():
            x = ord(ch.upper()) - 65
            y = (x + k) % 26
            rows.append({"Letter": ch.upper(), "P": x, "P + k": x + k, "(P + k) mod 26": y, "Cipher letter": chr(y + 65)})
    if rows:
        st.dataframe(rows)
        st.success("Ciphertext: " + "".join(r["Cipher letter"] for r in rows))
        st.caption("When P + k passes 25, mod 26 wraps it back to the start of the alphabet.")

with t2:
    st.latex(r"E(x) = (a x + b) \bmod 26 \qquad D(y) = a^{-1}(y - b) \bmod 26")
    a = st.selectbox("a", list(range(1, 26)), index=4)
    b = st.slider("b", 0, 25, 8)
    g = nt.gcd(a, 26)
    distinct = len({(a * x + b) % 26 for x in range(26)})
    c1, c2, c3 = st.columns(3)
    c1.metric("gcd(a, 26)", g)
    c2.metric("Distinct outputs", f"{distinct} / 26")
    c3.metric("Bijective?", "Yes" if distinct == 26 else "No")
    if g == 1:
        st.success(f"a = {a} is coprime with 26, so every letter maps to a different letter and decryption works. Inverse: a⁻¹ = {nt.mod_inverse(a, 26)}")
        w = st.text_input("Word", "AFFINE", key="a_word")
        st.write("Ciphertext:", affine.encrypt(w, a, b))
    else:
        st.error(f"gcd({a}, 26) = {g}, not 1. Some letters collide, so the function is not one-to-one and cannot be decrypted.")
    st.write(f"Valid values of a: {affine.VALID_A}. That is {len(affine.VALID_A)} = φ(26) values, so the key space is {len(affine.VALID_A)} × 26 = {len(affine.VALID_A) * 26}.")

with t3:
    st.caption("Small primes, so you can follow every step by hand.")
    c1, c2, c3, c4 = st.columns(4)
    p = c1.number_input("p (prime)", min_value=2, value=61, step=1)
    q = c2.number_input("q (prime)", min_value=2, value=53, step=1)
    e = c3.number_input("e", min_value=2, value=17, step=1)
    m = c4.number_input("Message m (a number)", min_value=0, value=65, step=1)
    if p == q or not (nt.is_prime(p) and nt.is_prime(q)):
        st.warning("p and q must be two different primes.")
    else:
        n, phi = p * q, (p - 1) * (q - 1)
        st.write(f"**Step 1:** n = p × q = {p} × {q} = **{n}**")
        st.write(f"**Step 2:** φ(n) = (p − 1)(q − 1) = {p - 1} × {q - 1} = **{phi}**")
        g = nt.gcd(e, phi)
        if g != 1 or e >= phi:
            st.warning(f"**Step 3:** e must satisfy 1 < e < φ(n) and gcd(e, φ(n)) = 1. Here gcd({e}, {phi}) = {g}.")
        elif m >= n:
            st.warning(f"The message m must be smaller than n = {n}.")
        else:
            d = nt.mod_inverse(e, phi)
            c = nt.mod_exp(m, e, n)
            back = nt.mod_exp(c, d, n)
            st.write(f"**Step 3:** gcd({e}, {phi}) = 1, so e is valid.")
            st.write(f"**Step 4:** d = e⁻¹ mod φ(n) = **{d}** (check: {e} × {d} = {e * d} ≡ {(e * d) % phi} mod {phi})")
            st.write(f"**Public key:** ({n}, {e}) and **private key:** ({n}, {d})")
            st.write(f"**Step 5 (encrypt):** c = m^e mod n = {m}^{e} mod {n} = **{c}**")
            st.write(f"**Step 6 (decrypt):** m = c^d mod n = {c}^{d} mod {n} = **{back}**")
            if back == m:
                st.success("The decrypted value equals the original message.")

with t4:
    st.subheader("Key spaces (counting)")
    spaces = {
        "Caesar": 26,
        "Affine": 12 * 26,
        "Vigenère (4-letter keyword)": 26 ** 4,
        "Substitution cipher (any permutation of 26 letters)": math.factorial(26),
        "AES-256": 2 ** 256,
    }
    st.dataframe([{"Cipher": name, "Number of keys": f"{v:,}" if v < 10 ** 12 else f"{v:.3e}",
                   "Bits": round(math.log2(v), 1)} for name, v in spaces.items()])

    st.subheader("Permutations and combinations")
    kk = st.slider("Keyword length", 1, 10, 4)
    st.write(f"Keywords, repeated letters allowed: 26^{kk} = {26 ** kk:,}")
    st.write(f"Keywords with all different letters, P(26, {kk}) = {math.perm(26, kk):,}")
    st.write(f"Ways to pick {kk} letters, order ignored, C(26, {kk}) = {math.comb(26, kk):,}")

    st.subheader("Derangements")
    nn = st.slider("Alphabet size", 2, 26, 26)
    D = sum((-1) ** i * math.factorial(nn) // math.factorial(i) for i in range(nn + 1))
    st.write(f"A substitution cipher that maps no letter to itself is a derangement. D({nn}) = {D:,} out of {math.factorial(nn):,} permutations, a fraction of {D / math.factorial(nn):.4f} (about 1/e).")

    st.subheader("Sets and Euler's phi function")
    n = int(st.number_input("n", min_value=2, max_value=5000, value=26, step=1))
    U = [x for x in range(1, n) if nt.gcd(x, n) == 1]
    if n <= 60:
        st.write("Units mod n (numbers coprime to n): U = {" + ", ".join(map(str, U)) + "}")
    st.write(f"|U| = {len(U)}")
    fs = prime_factors(n)
    terms, total = [], 0
    for r in range(len(fs) + 1):
        for combo in itertools.combinations(fs, r):
            term = (-1) ** r * (n // math.prod(combo))
            total += term
            terms.append(("+ " if term >= 0 else "− ") + str(abs(term)))
    st.write(f"Prime factors of {n}: {fs}")
    st.write("Inclusion-exclusion: φ(n) = " + " ".join(terms).lstrip("+ ") + f" = **{total}**")
    st.caption(f"Matches |U| = {len(U)} and the totient function: {nt.totient(n)}.")

with t5:
    st.subheader("XOR truth table")
    rows = []
    for P, Q in itertools.product([0, 1], repeat=2):
        rows.append({"P": P, "Q": Q, "P XOR Q": P ^ Q,
                     "(P OR Q) AND NOT (P AND Q)": int(bool((P or Q) and not (P and Q))),
                     "(P XOR Q) XOR Q": (P ^ Q) ^ Q})
    st.dataframe(rows)
    st.caption("Columns 3 and 4 are identical, so XOR is logically equivalent to (P ∨ Q) ∧ ¬(P ∧ Q). The last column equals P: XOR-ing twice with the same key restores the message.")

    st.subheader("Congruence mod n is an equivalence relation")
    mod = st.slider("n", 2, 12, 5)
    S = range(15)
    R = {(x, y) for x in S for y in S if (x - y) % mod == 0}
    refl = all((x, x) in R for x in S)
    sym = all((y, x) in R for (x, y) in R)
    trans = all((x, z) in R for (x, y) in R for (y2, z) in R if y == y2)
    st.write(f"On the set {{0, ..., 14}}: reflexive {'✓' if refl else '✗'}, symmetric {'✓' if sym else '✗'}, transitive {'✓' if trans else '✗'}")
    for r in range(mod):
        st.write(f"[{r}] = {{" + ", ".join(str(x) for x in S if x % mod == r) + "}")
    st.caption(f"It splits the set into {mod} equivalence classes. Caesar, Affine and RSA all work with these classes.")

    st.subheader("Pigeonhole principle (hash collisions)")
    st.write("A hash maps unlimited inputs to a fixed number of outputs. We shrink SHA-256 to 8 bits (256 possible outputs), so by pigeonhole any 257 inputs must contain a collision.")
    seen = {}
    for i in range(257):
        h = hashing.sha256_hex(f"message {i}".encode())[:2]
        if h in seen:
            st.success(f"Collision found: 'message {seen[h]}' and 'message {i}' both give {h}.")
            break
        seen[h] = i