from Crypto.Random import get_random_bytes
from Crypto.Util.strxor import strxor
import base64

cipher_base64 = "cHduLmNvbGxlZ2V7Y2R4SkRoQkQ2UnNSeGZJMW9UUmxsTjA4SVRILmRWek56TURMM1VqTjJNeld9Cg=="
cipher = base64.b64decode(cipher_base64)
