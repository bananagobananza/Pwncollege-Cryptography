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


