import base64

c = "0rwAfvb53QWuiZLhNGZfSBwXzXrajKW6jZX5RURZYMIo2hyNRA2h/dr7ZI1jwFBQaDtEHKQ0HEUPXw=="
cdc = base64.b64decode(c)
for i in range (0, 256):
    ans = ""
    for j in range (0, len(cdc)):
        ans += chr(cdc[j] ^ i)
    print(ans)
    if ans.startswith("pwn"):
        print(ans)
        break

plain = "Yg=="
cipher = "wA=="
plain_decoded = base64.b64decode(plain)
cipher_decoded = base64.b64decode(cipher)
print(plain_decoded)
print(cipher_decoded)
print(plain_decoded[0] ^ cipher_decoded[0])

#WU: a xor b = c => c xor a = b

