import sys
import string
import random
import pathlib
import base64
import json
import textwrap

from Crypto.Cipher import AES
from Crypto.Hash.SHA256 import SHA256Hash
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Random.random import getrandbits, randrange
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad, unpad


flag = "Congrat"
config = (pathlib.Path(__file__).parent / ".config").read_text()
level = int(config)


def show(name, value, *, b64=True):
    print(f"{name}: {value}")


def show_b64(name, value):
    show(f"{name} (b64)", base64.b64encode(value).decode())


def show_hex(name, value):
    show(name, hex(value))


def input_(name):
    try:
        return input(f"{name}: ")
    except (KeyboardInterrupt, EOFError):
        print()
        exit(0)


def input_b64(name):
    data = input_(f"{name} (b64)")
    try:
        return base64.b64decode(data)
    except base64.binascii.Error:
        print(f"Failed to decode base64 input: {data!r}", file=sys.stderr)
        exit(1)


def input_hex(name):
    data = input_(name)
    try:
        return int(data, 16)
    except Exception:
        print(f"Failed to decode hex input: {data!r}", file=sys.stderr)
        exit(1)


def level1():
    """
    In this challenge you will decode base64 data.
    Despite base64 data appearing "mangled", it is not an encryption scheme.
    It is an encoding, much like base2, base10, base16, and ascii.
    It is a popular way of encoding raw bytes.
    """
    show_b64("flag", flag)


def level2():
    """
    In this challenge you will decrypt a secret encrypted with a one-time pad.
    Although simple, this is the most secure encryption mechanism, if you could just securely transfer the key.
    """
    key = get_random_bytes(len(flag))
    ciphertext = strxor(flag, key)
    show_b64("key", key)
    show_b64("secret ciphertext", ciphertext)


def level3():
    """
    In this challenge you will decrypt a secret encrypted with a one-time pad.
    You can encrypt arbitrary data, with the key being reused each time.
    """
    key = get_random_bytes(256)
    assert len(flag) <= len(key)

    ciphertext = strxor(flag, key[:len(flag)])
    show_b64("secret ciphertext", ciphertext)

    while True:
        plaintext = input_b64("plaintext")
        ciphertext = strxor(plaintext, key[:len(plaintext)])
        show_b64("ciphertext", ciphertext)


def level4():
    """
    In this challenge you will decrypt a secret encrypted with Advanced Encryption Standard (AES).
    The Electronic Codebook (ECB) block cipher mode of operation is used.
    """
    key = get_random_bytes(16)
    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(flag, cipher.block_size))
    show_b64("key", key)
    show_b64("secret ciphertext", ciphertext)



def level5():
    """
    In this challenge you will decrypt a secret encrypted with Advanced Encryption Standard (AES).
    The Electronic Codebook (ECB) block cipher mode of operation is used.
    You can encrypt arbitrary data, which has the secret appended to it, with the key being reused each time.
    """
    key = get_random_bytes(16)
    cipher = AES.new(key=key, mode=AES.MODE_ECB)

    ciphertext = cipher.encrypt(pad(flag, cipher.block_size))
    show_b64("secret ciphertext", ciphertext)

    while True:
        plaintext_prefix = input_b64("plaintext prefix")
        ciphertext = cipher.encrypt(pad(plaintext_prefix + flag, cipher.block_size))
        show_b64("ciphertext", ciphertext)


def level6():
    """
    In this challenge you will perform a Diffie-Hellman key exchange.
    """
    # 2048-bit MODP Group from RFC3526
    p = int.from_bytes(bytes.fromhex(
        "FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 "
        "29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD "
        "EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245 "
        "E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED "
        "EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D "
        "C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F "
        "83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D "
        "670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B "
        "E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 "
        "DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510 "
        "15728E5A 8AACAA68 FFFFFFFF FFFFFFFF"
    ), "big")
    g = 2

    show_hex("p", p)
    show_hex("g", g)

    a = getrandbits(2048)
    A = pow(g, a, p)
    show_hex("A", A)

    B = input_hex("B")
    if not (B > 2**1024):
        print("Invalid B value (B > 2**1024)", file=sys.stderr)
        exit(1)

    s = pow(B, a, p)

    key = s.to_bytes(256, "little")
    assert len(flag) <= len(key)
    ciphertext = strxor(flag, key[:len(flag)])
    show_b64("secret ciphertext", ciphertext)


def level7():
    """
    In this challenge you will decrypt a secret encrypted with RSA (Rivest–Shamir–Adleman).
    You will be provided with both the public key and private key.
    """
    key = RSA.generate(2048)
    assert len(flag) <= 256
    ciphertext = pow(int.from_bytes(flag, "little"), key.e, key.n).to_bytes(256, "little")
    show_hex("e", key.e)
    show_hex("d", key.d)
    show_hex("n", key.n)
    show_b64("secret ciphertext", ciphertext)


def level8():
    """
    In this challenge you will decrypt a secret encrypted with RSA (Rivest–Shamir–Adleman).
    You will be provided with the prime factors of n.
    """
    key = RSA.generate(2048)
    assert len(flag) <= 256
    ciphertext = pow(int.from_bytes(flag, "little"), key.e, key.n).to_bytes(256, "little")
    show_hex("e", key.e)
    show_hex("p", key.p)
    show_hex("q", key.q)
    show_b64("secret ciphertext", ciphertext)


def level9():
    """
    In this challenge you will hash data with a Secure Hash Algorithm (SHA256).
    You will find a small hash collision.
    Your goal is to find data, which when hashed, has the same hash as the secret.
    Only the first 2 bytes of the SHA256 hash are considered.
    """
    prefix_length = 2
    sha256 = SHA256Hash(flag).digest()
    show_b64(f"secret sha256[:{prefix_length}]", sha256[:prefix_length])

    collision = input_b64("collision")
    if SHA256Hash(collision).digest()[:prefix_length] == sha256[:prefix_length]:
        show("flag", flag.decode())


def level10():
    """
    In this challenge you will hash data with a Secure Hash Algorithm (SHA256).
    You will compute a small proof-of-work.
    Your goal is to find response data, which when appended to the challenge data and hashed, begins with 2 null-bytes.
    """
    difficulty = 2

    challenge = get_random_bytes(32)
    show_b64("challenge", challenge)

    response = input_b64("response")
    if SHA256Hash(challenge + response).digest()[:difficulty] == (b'\0' * difficulty):
        show("flag", flag.decode())


def level11():
    """
    In this challenge you will complete an RSA challenge-response.
    You will be provided with both the public key and private key.
    """
    key = RSA.generate(2048)

    show_hex("e", key.e)
    show_hex("d", key.d)
    show_hex("n", key.n)

    challenge = int.from_bytes(get_random_bytes(256), "little") % key.n
    show_hex("challenge", challenge)

    response = input_hex("response")
    if pow(response, key.e, key.n) == challenge:
        show("flag", flag.decode())


def level12():
    """
    In this challenge you will complete an RSA challenge-response.
    You will provide the public key.
    """
    e = input_hex("e")
    n = input_hex("n")

    if not (e > 2):
        print("Invalid e value (e > 2)", file=sys.stderr)
        exit(1)

    if not (2**512 < n < 2**1024):
        print("Invalid n value (2**512 < n < 2**1024)", file=sys.stderr)
        exit(1)

    challenge = int.from_bytes(get_random_bytes(64), "little")
    show_hex("challenge", challenge)

    response = input_hex("response")
    if pow(response, e, n) == challenge:
        ciphertext = pow(int.from_bytes(flag, "little"), e, n).to_bytes(256, "little")
        show_b64("secret ciphertext", ciphertext)


def level13():
    """
    In this challenge you will work with public key certificates.
    You will be provided with a self-signed root certificate.
    You will also be provided with the root private key, and must use that to sign a user certificate.
    """
    root_key = RSA.generate(2048)

    show_hex("root key d", root_key.d)

    root_certificate = {
        "name": "root",
        "key": {
            "e": root_key.e,
            "n": root_key.n,
        },
        "signer": "root",
    }

    root_trusted_certificates = {
        "root": root_certificate,
    }

    root_certificate_data = json.dumps(root_certificate).encode()
    root_certificate_hash = SHA256Hash(root_certificate_data).digest()
    root_certificate_signature = pow(
        int.from_bytes(root_certificate_hash, "little"),
        root_key.d,
        root_key.n
    ).to_bytes(256, "little")

    show_b64("root certificate", root_certificate_data)
    show_b64("root certificate signature", root_certificate_signature)

    user_certificate_data = input_b64("user certificate")
    user_certificate_signature = input_b64("user certificate signature")

    try:
        user_certificate = json.loads(user_certificate_data)
    except json.JSONDecodeError:
        print("Invalid user certificate", file=sys.stderr)
        exit(1)

    user_name = user_certificate.get("name")
    if user_name in root_trusted_certificates:
        print(f"Invalid user certificate name: `{user_name}`", file=sys.stderr)
        exit(1)

    user_key = user_certificate.get("key", {})
    if not (isinstance(user_key.get("e"), int) and isinstance(user_key.get("n"), int)):
        print(f"Invalid user certificate key: `{user_key}`", file=sys.stderr)
        exit(1)

    if not (user_key["e"] > 2):
        print("Invalid user certificate key e value (e > 2)", file=sys.stderr)
        exit(1)

    if not (2**512 < user_key["n"] < 2**1024):
        print("Invalid user certificate key n value (2**512 < n < 2**1024)", file=sys.stderr)
        exit(1)

    user_signer = user_certificate.get("signer")
    if user_signer not in root_trusted_certificates:
        print(f"Untrusted user certificate signer: `{user_signer}`", file=sys.stderr)
        exit(1)

    user_signer_key = root_trusted_certificates[user_signer]["key"]
    user_certificate_hash = SHA256Hash(user_certificate_data).digest()
    user_certificate_check = pow(
        int.from_bytes(user_certificate_signature, "little"),
        user_signer_key["e"],
        user_signer_key["n"]
    ).to_bytes(256, "little")[:len(user_certificate_hash)]

    if user_certificate_check != user_certificate_hash:
        print("Untrusted user certificate: invalid signature", file=sys.stderr)
        exit(1)

    ciphertext = pow(int.from_bytes(flag, "little"), user_key["e"], user_key["n"]).to_bytes(256, "little")
    show_b64("secret ciphertext", ciphertext)


def level14():
    """
    In this challenge you will perform a simplified Transport Layer Security (TLS) handshake, acting as the server.
    You will be provided with Diffie-Hellman parameters, a self-signed root certificate, and the root private key.
    The client will request to establish a secure channel with a particular name, and initiate a Diffie-Hellman key exchange.
    The server must complete the key exchange, and derive an AES-128 key from the exchanged secret.
    Then, using the encrypted channel, the server must supply the requested user certificate, signed by root.
    Finally, using the encrypted channel, the server must sign the handshake to prove ownership of the private user key.
    """
    # 2048-bit MODP Group from RFC3526
    p = int.from_bytes(bytes.fromhex(
        "FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 "
        "29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD "
        "EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245 "
        "E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED "
        "EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D "
        "C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F "
        "83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D "
        "670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B "
        "E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 "
        "DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510 "
        "15728E5A 8AACAA68 FFFFFFFF FFFFFFFF"
    ), "big")
    g = 2

    show_hex("p", p)
    show_hex("g", g)

    root_key = RSA.generate(2048)

    show_hex("root key d", root_key.d)

    root_certificate = {
        "name": "root",
        "key": {
            "e": root_key.e,
            "n": root_key.n,
        },
        "signer": "root",
    }

    root_trusted_certificates = {
        "root": root_certificate,
    }

    root_certificate_data = json.dumps(root_certificate).encode()
    root_certificate_hash = SHA256Hash(root_certificate_data).digest()
    root_certificate_signature = pow(
        int.from_bytes(root_certificate_hash, "little"),
        root_key.d,
        root_key.n
    ).to_bytes(256, "little")

    show_b64("root certificate", root_certificate_data)
    show_b64("root certificate signature", root_certificate_signature)

    name = ''.join(random.choices(string.ascii_lowercase, k=16))
    show("name", name)

    a = getrandbits(2048)
    A = pow(g, a, p)
    show_hex("A", A)

    B = input_hex("B")
    if not (B > 2**1024):
        print("Invalid B value (B > 2**1024)", file=sys.stderr)
        exit(1)

    s = pow(B, a, p)
    key = SHA256Hash(s.to_bytes(256, "little")).digest()[:16]
    cipher_encrypt = AES.new(key=key, mode=AES.MODE_CBC, iv=b"\0"*16)
    cipher_decrypt = AES.new(key=key, mode=AES.MODE_CBC, iv=b"\0"*16)

    def decrypt_input_b64(name):
        data = input_b64(name)
        try:
            return unpad(cipher_decrypt.decrypt(data), cipher_decrypt.block_size)
        except ValueError as e:
            print(f"{name}: {e}", file=sys.stderr)
            exit(1)

    user_certificate_data = decrypt_input_b64("user certificate")
    user_certificate_signature = decrypt_input_b64("user certificate signature")
    user_signature = decrypt_input_b64("user signature")

    try:
        user_certificate = json.loads(user_certificate_data)
    except json.JSONDecodeError:
        print("Invalid user certificate", file=sys.stderr)
        exit(1)

    user_name = user_certificate.get("name")
    if user_name != name:
        print(f"Invalid user certificate name: `{user_name}`", file=sys.stderr)
        exit(1)

    user_key = user_certificate.get("key", {})
    if not (isinstance(user_key.get("e"), int) and isinstance(user_key.get("n"), int)):
        print(f"Invalid user certificate key: `{user_key}`", file=sys.stderr)
        exit(1)

    if not (user_key["e"] > 2):
        print("Invalid user certificate key e value (e > 2)", file=sys.stderr)
        exit(1)

    if not (2**512 < user_key["n"] < 2**1024):
        print("Invalid user certificate key n value (2**512 < n < 2**1024)", file=sys.stderr)
        exit(1)

    user_signer = user_certificate.get("signer")
    if user_signer not in root_trusted_certificates:
        print(f"Untrusted user certificate signer: `{user_signer}`", file=sys.stderr)
        exit(1)

    user_signer_key = root_trusted_certificates[user_signer]["key"]
    user_certificate_hash = SHA256Hash(user_certificate_data).digest()
    user_certificate_check = pow(
        int.from_bytes(user_certificate_signature, "little"),
        user_signer_key["e"],
        user_signer_key["n"]
    ).to_bytes(256, "little")[:len(user_certificate_hash)]

    if user_certificate_check != user_certificate_hash:
        print("Untrusted user certificate: invalid signature", file=sys.stderr)
        exit(1)

    user_signature_data = (
        name.encode().ljust(256, b"\0") +
        A.to_bytes(256, "little") +
        B.to_bytes(256, "little")
    )
    user_signature_hash = SHA256Hash(user_signature_data).digest()
    user_signature_check = pow(
        int.from_bytes(user_signature, "little"),
        user_key["e"],
        user_key["n"]
    ).to_bytes(256, "little")[:len(user_signature_hash)]

    if user_signature_check != user_signature_hash:
        print("Untrusted user: invalid signature", file=sys.stderr)
        exit(1)

    ciphertext = cipher_encrypt.encrypt(pad(flag, cipher_encrypt.block_size))
    show_b64("secret ciphertext", ciphertext)


def challenge():
    challenge_level = globals()[f"level{level}"]
    description = textwrap.dedent(challenge_level.__doc__)

    print("===== Welcome to Cryptography! =====")
    print("In this series of challenges, you will be working with various cryptographic mechanisms.")
    print(description)
    print()

    challenge_level()


challenge()