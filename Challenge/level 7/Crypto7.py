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

# Your RSA keys
e = 0x10001
d = 0x32e0009af334c28ed28d879e5b074aa4223aaa4ab0bdd5a20c975ba5092dbfea668266e28a6c70549619334bd35edd7f303a0bb51c249442f61cd0d3c51afd1a63de5d4d2862505b7334b4993858ab1c81b8a74d21e73c91a9ee59b5a3b8bbc6e9eca7944984fe976ffff10a32815083012bb968448163a1a5d26d29d5fb9cd39ed8a5eac48429cb1c430eb24beeb6b74e4f401f9d23431b6a28fe311934cbc7bc7a4dc76db1c368151cf200cc094717dd73212f3f79cb7c9c4d3d3e2112360468d89bce0c32f0eb34d57cacc714b4008fe6251ee55447d5387bd9e84f68a307500bca9e14f6f0b0fa261bd3279ba5d859ca060d182645edf4a9ed630ac37179
n = 0x948cb1bbdc46300f05c38d4dab234bf76ed0a93ad4ad073215b5a91dbe73011ba9dfa58a838a8d99fe2085a3f0edfa408d8915779c03b3363cf8dbffbf911229813f01bd577c9d826b3130bc4b9e45278d8bc9babc5b74b9705b7822bc3296fbecbe09111c0fa65b4083c52025b96ef24c55c11bee744555ddf18c8261372dad4712a837a921318334b156114f9a608f8e12da0231ff788771f37abf40905f9ada95a574456e690ae59318a4821664e51f1246976eb23f028d573837e8876324aaf22db89730f3f8ed872dd0f1de4355f5a8d5a35ab57d4ff896d047dddd381985e350a642a0d1f7002fff1da87daf5b27c509e2e8e831cc37b002530bbe1427

# Your ciphertext in base64 format
b64_ciphertext = "qnd9HxMiwispG5yb32TWGnpsMtDla096NERDEHA/77hSb4QMsQh4eiHzK7xU8bbAT2ndUSPWpzX/7ji4iT1YMVG16fZugNanGr2DQAqe4/G79Mz5JM7f0kkZquGeV24Zp3TM7108bz5oYaIQsCDZRrNiid6jOBGxjCSLVZulVbpT17sFxdG5DLGHQpBUGtC8RNILsyz/4dLwznMGOLpjsKp2ls5QVy3cWT95bPMVRy5+3CBmEqFR1wAKxx1rbZE8hLaDwSCGGZDaQBqgSOzQaa08fr43c1lpzTGIIQ2aI7oA+nv5jjemtEaHPGsp4zS7xP+rFORj+lnyPjgUNxjPhQ=="

# Decode the ciphertext from base64
ciphertext = base64.b64decode(b64_ciphertext)

# Decrypt the ciphertext
plaintext = decrypt_rsa(ciphertext, (d, n))

# Print the plaintext
string = plaintext.decode('utf-8')
print(string)
