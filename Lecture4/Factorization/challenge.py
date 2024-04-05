#!/usr/bin/env python3
import os
import random
from Crypto.Util.number import getPrime, isPrime, bytes_to_long

if os.path.exists("./flag.txt"):
    with open("./flag.txt", "rb") as f:
        FLAG = f.read().strip()
else:
    FLAG = b"UniTN{placeholder_flag}"


p = getPrime(1024)
q = p + 1
while not isPrime(q):
    q += random.randint(1, 10000)

n = p * q
e = 65537

m = bytes_to_long(FLAG)
c = pow(m, e, n)
with open("message.txt", "w") as f:
    f.write(f"{n}\n{e}\n{c}\n")
