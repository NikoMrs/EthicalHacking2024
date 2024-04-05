from gmpy2 import iroot

with open("message.txt", "r") as f:
    n = f.readline()
    e = int(f.readline())
    c = int(f.readline())

m = iroot(c, e)
print(m[0])