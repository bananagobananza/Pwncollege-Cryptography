from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def encrypt(flag):
    #blocksize = 16
    key = b"Sup3r_S3cr3t!!!!"
    assert len(key) == 16
    cipher = AES.new(key = key, mode = AES.MODE_ECB)
    flag = pad(flag, 16)
    ciphertext = cipher.encrypt(flag)
    return base64.b64encode(ciphertext)

flag = b"pwn.college{practice}"
flag = pad(flag, 16)
#print(flag)
secrettext = "J0iSC8HwAILxQRk1vAtXfREysHhTodUsV3SjxB492ZE="
#encrypt(flag)

flagenc = base64.b64decode(secrettext)

knownflag = ""
anschar = ""

for i in range (16):
    text = (knownflag + "A" * (15 - i) + flag[0:16].decode())[:16]
    text = text.encode()
    for j in range (256):
        check = (knownflag + "A" * (15 - i) + anschar + chr(j)).encode()
        if encrypt(check) == encrypt(text): 
            anschar += chr(j)
            break
    print(anschar)

print(len("YjjMoT8p9HXlo/aYl0pKwpqKbdO7EhAiXtyYutuFQP"))