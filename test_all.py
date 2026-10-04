import number_theory as nt, caesar, vigenere, xor_cipher, rsa, aes

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

def test_rsa():
    k = rsa.generate_keys(512)
    msg = "Discrete Maths rocks! " * 10
    assert rsa.decrypt(rsa.encrypt(msg, k["n"], k["e"]), k["n"], k["d"]) == msg

def test_aes():
    assert aes.decrypt(aes.encrypt(b"hello", "pw"), "pw") == b"hello"
    try:
        aes.decrypt(aes.encrypt(b"hello", "pw"), "wrong")
        assert False
    except Exception:
        pass

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)