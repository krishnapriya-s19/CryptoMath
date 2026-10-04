# DM concepts used
- Euler's phi: rsa.py (phi = (p-1)(q-1)), number_theory.totient
- Bijective functions: every cipher is a bijection; decrypt is the inverse
- Equivalence relation: congruence mod n (caesar.py, vigenere.py, rsa.py)
- Propositional logic: xor_cipher.py (XOR truth table)
- Counting: key space sizes (26 for Caesar, 2^256 for AES)
- Pigeonhole: small key spaces force collisions/brute-force
- Also used: GCD, extended Euclid, primes (number_theory.py)