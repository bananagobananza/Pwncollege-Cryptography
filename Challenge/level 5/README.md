This problem involve know about AES-ECB mode 

1st step: the algorithm
- Basically AES-ECB mode divide the string (in this case flag) into blocks with the length given. (in this problem it is 16)
- It then encrypt the data inside the block then print out the encryption text, after which it will put it together and return the encypted text

2nd step: the exploitation
- In my Crypto5_algorithm.py, assume i have ```key = b"Sup3r_S3cr3t!!!!"``` which is 16 bytes.
- Assume i have the ```flag = b"pwn.college{practice}"``` after encryption i got ```b'J0iSC8HwAILxQRk1vAtXfREysHhTodUsV3SjxB492ZGfWsThqAId7Xq4EDpFwYEp'```
- Reading the problemm, it said that i can pad letter i want to the front of the orginal flag, then it will encrypt for us:
Ex: pad 4 A's to the front pwn.college{practice} -> AAAApwn.college{practice}.
- Only then it will encrypt. By this, we can bruteforce each letter of the flag. Since the blocksize is 16, we first try to add 15 A's to the front of the flag:
pwn.college{practice} -> AAAAAAAAAAAAAAApwn.college{practice}.
It then first encrypt the first 16 bytes, which is ```AAAAAAAAAAAAAAAp``` --> encryption = X
- We see that the first letter of the flag is now appear in the end of the block size, so by bruteforce using AES-ECB mode, we can find this letter by using AES-ECB to encrypt ```AAAAAAAAAAAAAAA + char(0 -> 255)``` to see which encryption match X.
- Now that we have optain the first letter, now moving to the second one. Since we already know the first one, we now only need to pad 14 A's to the front, because we want to maintain the blocksize = 16.
So in our example, padding 14 A's will encrypt ```AAAAAAAAAAAAAApw```.
And now we want to continue bruteforce the second letter using the same methode as the first one.
- After doing that 16 times, we will optain the first block - 16 bytes of the flag:

```
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
```
- So we have obtain the first block, now moving to the second block
we need to find the 17th byte of the flag, after already know the first 16. So we do the same as the first block, the only difference is now we want to brute force ```AAAAAAAAAAAAAAA + [1st block] + char(0 -> 255)```
to find the 17th byte after sending 15 A's. (the first block is ```AAAAAAAAAAAAAAAp``` and the second is ```wn.college{prac + char(0 -> 255)```)
- The rest of third, forth, ... block we will do the same.

~Discussion~
1. what happen if we want to pad % 16 != 0 ?
--> throw no bytes at the end 
Ex: "Helloworld" -> "Helloworld000000" -> no idea to determine
Solution: Put how much to pad at the end
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
...

3rd step: interactive with server
- Now the problem does not give us the flag, which me must interact with the server in order to brute force the flag
- The solution is similar to the 2nd step, but we will use pwn tool to improve our time process
