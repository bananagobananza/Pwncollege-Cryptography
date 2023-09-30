Explain: We are stading in Bob side, which is we have b and g^b in the begining. By having know A
we have:
flag xor (B ^ a  % p) = flag xor (A ^ b % p) 
<=> flag xor (g ^ ba % p) = flag xor (g ^ ab % p) 

We already have g and p, now we only need to generate a random b
and get B = pow(g, b, p)