Basically the problem give you a secret cipher text (let's call cipher) which is:
    flag ^ key = cipher
And the problem also give you ability to xor a base64 string using the same key
So we just need to remember:
    flag ^ key = cipher
=>  cipher ^ key = flag

So we imput the string as the cipher, and it will return ```cHduLmNvbGxlZ2V7Y2R4SkRoQkQ2UnNSeGZJMW9UUmxsTjA4SVRILmRWek56TURMM1VqTjJNeld9Cg==``` for us
decode it using b64 decoder ==> flag!