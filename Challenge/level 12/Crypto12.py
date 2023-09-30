import base64

from Crypto.Util.number import getPrime

def decrypt_rsa(ciphertext, private_key):
    d, n = private_key
    ciphertext = int.from_bytes(ciphertext, byteorder='little')
    plaintext = pow(ciphertext, d, n)
    plaintext = plaintext.to_bytes((plaintext.bit_length() + 7) // 8, byteorder='little')
    return plaintext

#p = getPrime(512)
#q = getPrime(512)
p = 9179377503990989755801406920315918050050669505869402560544119930217661952090841967893581805377601419478549085087062867117254128759547803500395614927160427
q = 11141700565866907102518761213248597837870054043736815654009254808280579617530997550751000525195211957486634665090568134306522344087185821585012276807926613

n = p * q
e = 3

c = 0x9d2e5904be14a77884ed4df5d988f2b0168345eb1ae6e7d72626d21bfda7b63d24ce592a2ec2c190568e2051b1a1e1d6023aff584bfcc90faaf95253b5960303

phi = (p - 1) * (q - 1)

d = pow(e, -1, phi)
#print(hex(pow(c, d, n)))

flag_cipher = "0+ICyM9b9vxwv3NlOSPZAfgn5aUTHndlD8HGKHMJyTSstuvvP4Zks7/+J5ylAiTyNcaiXZkdWswkJtk+h30GPynFhkE88TjBx5GUwn2t1YzizbwcU6M2es5kSQZDriXdtMfQFFxvC3HZETWifQwSfDHDzD8hRcFvDkWwN6BNTB8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="

flag = base64.b64decode(flag_cipher)
plain_text = decrypt_rsa(flag, (d, n))
print(plain_text)