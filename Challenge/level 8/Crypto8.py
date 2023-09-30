import base64

def decrypt_rsa(ciphertext, private_key):
    # Unpack the private key into its components
    d, n = private_key
    # Convert the ciphertext into a number
    ciphertext = int.from_bytes(ciphertext, byteorder='little')
    # Decrypt the ciphertext with the private key
    plaintext = pow(ciphertext, d, n)
    # Convert the plaintext from a number back into a string
    plaintext = plaintext.to_bytes((plaintext.bit_length() + 7) // 8, byteorder='little')
    return plaintext

e = 0x10001
p = 0xd32d59fc7b3de5cba1b2214a2957b043b112618044863b823eaceef4dc7e807ca1093353f7e7e80232c1ad2e32095a76991421a4886e549833f2596c15730e6d355845d8b97ba435efc0cb0ae38a9244b6f914755edfe53384ebf5b10dfea6f9222d8a253f8e5a439f93d905d484cc91a78522f8f0c1d0cfa24c17a6f91ef46f
q = 0xe998913410f7993bd6283b29f01024a9fa1536e27dbbdb2e7a97840a904a58ec9b84a0b63081eedc5a4beebcfa8173400e14ba5baa2cc96eaa53cbd7bc18a6b09729ba701f3c7071eaead1c6b732ac2f5f718baf32d29fe5e6ec5760deb6b5e2c5b8dfe5e927d98a3896eab0c0dc3d1462351c3a0946ebecfb1af55459c51beb
ct = "mjcm3If02xepqgCUqmziBBOxkZr3Vfi5pT2LZg3FUxBvYzMgtQVu3qn7aNDJRLspNW2xv2mzjd71raXM2ZsHAugBcyJ2Raw3WAQkyIR5Sa38KHTDXcND47IXORpWZ9FvfcxU+ecOq4r5lJl8Zj5uSV0XrI6VJ1FTHIiC/DowS51wiRxsFf8A88MYzMZEj4zSR0CbN4v+6KBlUjjTfIXLNorR9boSQ8mmKFrSGscrqSwD4HPpHrCWUH1OehdeZzeTcSe17UhdZ1NnDqc+P5tNs7pNGnl8T9FvDEKnEKzoG7gf0EskDXoHUduSH9HDTSIymSn+BnCF80zRayLaF9lkag=="

ct = base64.b64decode(ct)

phi = (p - 1) * (q - 1)
n = p * q
d = pow(e, -1, phi)

plain_text = decrypt_rsa(ct, (d, n))

string = plain_text.decode("utf-8")
print(string)


