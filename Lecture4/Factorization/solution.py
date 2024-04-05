import math
from Crypto.Util.number import long_to_bytes

with open("message.txt", "r") as f:
    n = int(f.readline())
    e = int(f.readline())
    c = int(f.readline())

p = q = math.isqrt(n)
while True:
    if p * q == n:
        break
    p -= 1
    while(p*q  < n):
        q += 1

d = pow(e, -1, (p-1)*(q-1))
m = pow(c, d, n)

print(f"Difference between p and q: {q-p}")
print(f"Flag: {long_to_bytes(m).decode()}")