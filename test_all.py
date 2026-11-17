import number_theory as nt, caesar, vigenere, xor_cipher, rsa, aes
import affine, otp, chacha, hashing, strength, diffie_hellman as dh

def test_number_theory():
    assert nt.gcd(48, 18) == 6
    assert nt.mod_inverse(3, 11) == 4
    assert nt.mod_exp(4, 13, 497) == 445
    assert nt.is_prime(97) and not nt.is_prime(91)
    assert nt.totient(36) == 12

def test_classical():
    assert caesar.decrypt(caesar.encrypt("Hello, World!", 3), 3) == "Hello, World!"
    assert vigenere.encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
    assert vigenere.decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"
    x = xor_cipher.xor_bytes(b"secret", b"key")
    assert xor_cipher.xor_bytes(x, b"key") == b"secret"

def test_affine():
    assert affine.encrypt("AFFINE CIPHER", 5, 8) == "IHHWVC SWFRCP"
    assert affine.decrypt("IHHWVC SWFRCP", 5, 8) == "AFFINE CIPHER"
    assert len(affine.VALID_A) == 12
    try:
        affine.encrypt("abc", 2, 3)
        assert False
    except ValueError:
        pass

def test_otp():
    key = otp.generate_key(11)
    assert otp.decrypt(otp.encrypt("hello world", key), key) == "hello world"

def test_rsa():
    k = rsa.generate_keys(512)
    msg = "Discrete Maths rocks! " * 10
    assert rsa.decrypt(rsa.encrypt(msg, k["n"], k["e"]), k["n"], k["d"]) == msg
    k2 = rsa.import_keys(rsa.export_keys(k))
    assert k2["n"] == k["n"] and k2["d"] == k["d"]
    try:
        rsa.import_keys("not a key file")
        assert False
    except ValueError:
        pass

def test_aes_chacha():
    for mod in (aes, chacha):
        blob = mod.encrypt(b"hello", "pw")
        assert mod.decrypt(blob, "pw") == b"hello"
        try:
            mod.decrypt(blob, "wrong")
            assert False
        except Exception:
            pass

def test_hashing_dh_strength():
    assert hashing.sha256_hex(b"abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert hashing.avalanche("hello", "hellp") > 64
    p, g = dh.setup(32)
    a, A = dh.make_keypair(p, g)
    b, B = dh.make_keypair(p, g)
    assert dh.shared_secret(B, a, p) == dh.shared_secret(A, b, p)
    size, bits = strength.analyse("abc")
    assert size == 26 and strength.label(bits) == "Very weak"
    assert strength.analyse("Abc123!x")[0] == 95

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)