from hashlib import sha256
import base64

challenge = base64.b64decode("f9HWS0Q7bmTIjH4hIUzkY7L3D6xQFmshLTknkRugvcc=")

i = 0
while True:
    if sha256(challenge + str(i).encode()).digest()[:2] == b"\0\0":
        print(i)
        break
    i += 1

#bruteforce to find the matching [:2] == 2 null bytes
print(base64.b64encode(b"67558"))