# Diffie-Hellman key exchange

from Crypto.Random.random import getrandbits
from Crypto.Util.strxor import strxor
import base64

p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca18217c32905e462e36ce3be39e772c180e86039b2783a2ec07a28fb5c55df06f4c52c9de2bcbf6955817183995497cea956ae515d2261898fa051015728e5a8aacaa68ffffffffffffffff
g = 0x2
A = 0xc5f9f410c89762a9c3754940bddfd13d2290a03d010499e789497dbea07abab46da81f54b049fe86ad93873d668a9ff62d7429a5917a6825d1757e0290c21191336797c5b0e174737c5d1bf49128a3497e1321db2fbe5005627011545424a7ca3bfc518bbced193e87c169f1558a8611b5e583c18f86d9d8862bc63f71730b73f06b894b802284f79a9a85bf175dcc99f1aeee0a5c7ffe40f4aa5948e7d3b3a3e30603b4bb7f151e48a4bfdeae8bed153ee7d5a54047b593c25b96c38fe4a5d342a0b22da760e56c08557e0e5819d450a809d9eda98f9f063ad7fd436f055c11198c507fea410ad341b3b9b8bf0fd46a350e1c723f74fc307dd1c29db88abfba

b = getrandbits(2048)
B = pow(g, b, p)
print("b :", b)
print("B :", B)
print(hex(B))

secret_ct = "0mLRWzCO8yJIHIOP29d95nHKCyzoLn5qdpDugvdoOTFm9pAlq6FVsWpQ+STr79002oL4zEcX2M0z2A=="
secret = base64.b64decode(secret_ct)
print("SECRET :", secret)

s = pow(A, b, p)

key = s.to_bytes(256, "little")
print("KEY: ", key)
print(len(secret), len(key))
print("ANSWER :", strxor(secret, key[:58]))

