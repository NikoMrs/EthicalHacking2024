#!/usr/bin/env python3
import os
from Crypto.Util.number import getStrongPrime, bytes_to_long

if os.path.exists("./flag.txt"):
    with open("./flag.txt", "rb") as f:
        FLAG = f.read().strip()
else:
    FLAG = b"UniTN{placeholder_flag}"


p, q = getStrongPrime(512), getStrongPrime(512)
n = p * q
e = 3

m = bytes_to_long(FLAG)
c = pow(m, e, n)
with open("message.txt", "w") as f:
    f.write(f"{n}\n{e}\n{c}\n")
