'''
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def aes(plaintext, key):
    return "ciphertext"

key = b"Sup3r_S3cr3t!!!!"
assert len(key) == 16
cipher = AES.new(key = key, mode = AES.MODE_ECB)
plaintext = b"HELLO_WORLD_!!!!"
assert len(plaintext) == 16

ciphertext = cipher.encrypt(plaintext)

# print(plaintext)
# print(ciphertext)

                Discuss
1. what happen if we want to pad % 16 != 0 ?
--> throw no bytes at the end 
Ex: "Helloworld" -> "Helloworld000000" -> no idea to determine
Solution: Put how much padding at the end
Ex: "Helloworld" -> "Helloworld\x06\x06\x06\x06\x06\x06"
Ex2: print(pad(b"Hello, world!", 16))

2. Can only decrypt 16 bytes at a time (ECB: dealing with 16 bytes chunk)
plaintext = b"HELLO_World_12345678901234567890"
ciphertext = cipher.encrypt(plaintext)
print(plaintext)
for i in range (2):
    print(ciphertext[16 * i: 16 * (i + 1)].hex())

for i in range (2):
    ciphertext = cipher.encrypt(plaintext[16 * i: 16 * (i + 1)])
    print(ciphertext.hex())


                How to abuse the ECB mode
Using pwn tool
'''

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import pwn

pwn.context.update(encoding = "latin")
pwn.process("./run")
with pwn.process("./run") as process:
    process.readuntil("secret ciphertext (b64): ")
    ct = process.readline()
    print("The CT is:   ", ct)
    knownflag = ""
    process.readuntil("plaintext prefix (b64): ")
    for i in range (4):
        anschar = ""
        for j in range (16):
            insert = "A" * (15 - j) 
            print(insert)
            process.writeline(base64.b64encode(insert.encode()))
            process.readuntil("ciphertext (b64): ")
            text = process.readline()
            for k in range (256):
                check = ("A" * (15 - j) + knownflag + anschar + chr(k)).encode()
                print(k, " :", check)
                process.writeline(base64.b64encode(check))
                process.readuntil("ciphertext (b64): ")
                textcheck = process.readline()
                if base64.b64decode(textcheck)[16 * i:16 * (i+1)] == base64.b64decode(text)[16 * i:16 * (i+1)]:
                    anschar += chr(k)
                    break
        print("THE anschar is: ", anschar)  
        knownflag += anschar
    print("knownflag is :", knownflag)


