import secrets
from number_theory import generate_prime, mod_exp

def setup(bits=64):
    return generate_prime(bits), 5  # prime p and base g (demo values)

def make_keypair(p, g):
    private = secrets.randbelow(p - 3) + 2
    return private, mod_exp(g, private, p)

def shared_secret(their_public, my_private, p):
    return mod_exp(their_public, my_private, p)