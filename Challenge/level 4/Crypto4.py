from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def decrypt_aes(ciphertext, key):
    # Convert the key from base64 to bytes
    key = base64.b64decode(key)

    # Convert the ciphertext from base64 to bytes
    ciphertext_bytes = base64.b64decode(ciphertext)

    # Create a new AES cipher object with the key and AES.MODE_ECB mode
    cipher = AES.new(key, AES.MODE_ECB)

    # Decrypt the ciphertext
    plaintext_padded = cipher.decrypt(ciphertext_bytes)

    # Unpad the plaintext
    plaintext = unpad(plaintext_padded, AES.block_size)

    return plaintext.decode('utf-8')

# Example usage:
key = "EyQa3xu2mNdga4NfpJuYiA=="  # A 128-bit key
ciphertext = "wBoozXbZqM4DF9wApU3x+2PiQe7ryh0E8LAdWLvtkOB9pM+2VB9ifI+6QFLJtSzduVQCpgiw2nXr7a4Ohm0Zrg=="  # Base64-encoded ciphertext

print(decrypt_aes(ciphertext, key))
