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