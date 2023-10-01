The challenge give us:
- root key d
- root certificate --> decode to gain root key n
- root certificate signature

We want to provide our own certificate, which include:
- our own key: e, d, n
- our own json 
```
user_certificate = {
        "name": "Connor",
        "key": {
            "e": key_e, # our e
            "n": key_n  # our n
        },
        "signer": "root", # The code only trust root as signer
    }
```

After that, we want to sign our certificate
```
user_certificate_hash = SHA256Hash(json.dumps(user_certificate).encode()).digest()

user_certificate_signature = pow(
        int.from_bytes(user_certificate_hash, "little"),
        root_key_d,
        root_key_n
    ).to_bytes(256, "little")

```
Note that the signature s is calculate by:
```
    s = m^d (mod n)
with: - s: certificate
      - m: our certificate
      - d: we use private key (root key) 
      - n: the modulus provided by the server
```

After sending our certificate, we obtain the RSA flag encrypted using our e and n.
The decryption for RSA is:
```
    m = c^d (mod n)
with: - m: plaintext need to calculate
      - c: the encrypted RSA of flag
      - d: our private key (generate from the beginning)
      - n: our modulus (generate from the beginning)
```