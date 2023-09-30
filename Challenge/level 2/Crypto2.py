# import base64

# key = "meyOeetYZe5NY/4o0AfvnsmodBIY1XXPk25adtT8Ag8S8y/ntDjsvvRl1jcyDFmr2OFDk51+6ZBQyA=="
# ciphertxt = "6ZvgV4g3CYIoBJtTlWLd9qruN2EqsjT88AkbMPmXMXZToFm22EmUkJA3rHlIQR3n67Qp3a8zk8ctwg=="
# keydc = base64.b64decode(key)
# ciphertxtdc = base64.b64decode(ciphertxt)
# print(keydc)
# print(ciphertxtdc)
# for i in range (0, len(keydc)):
#     print(chr(keydc[i] ^ ciphertxtdc[i]), end = "")

import base64
import Crypto
from Crypto.Util.strxor import strxor

key = "meyOeetYZe5NY/4o0AfvnsmodBIY1XXPk25adtT8Ag8S8y/ntDjsvvRl1jcyDFmr2OFDk51+6ZBQyA=="
ciphertxt = "6ZvgV4g3CYIoBJtTlWLd9qruN2EqsjT88AkbMPmXMXZToFm22EmUkJA3rHlIQR3n67Qp3a8zk8ctwg=="
keydc = base64.b64decode(key)
ciphertxtdc = base64.b64decode(ciphertxt)

print(strxor(keydc, ciphertxtdc))
