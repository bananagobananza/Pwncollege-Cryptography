from hashlib import sha256
import base64

# Decode the base64 secret
secret_b64 = "y0E="
secret = base64.b64decode(secret_b64)

# Iterate over all possible 2-byte sequences
for i in range(256):
    for j in range(256):
        for k in range (256):
            # Generate a byte sequence
            ans = bytes([i, j, k])
            # Hash the byte sequence
            sha256_ans = sha256(ans).digest()
            # Compare the first 2 bytes of the hash with the secret
            if sha256_ans[:2] == secret[:2]:
                print(base64.b64encode(ans).decode())
                break

# basically bruteforce for 1, 2, 3, ... bytes char to find the matching sha256[:2]