import pwn
from Crypto.Util.number import long_to_bytes, bytes_to_long
import sys
sys.set_int_max_str_digits(50000)

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50302

if(REMOTE):
    conn = pwn.remote(IP_ADDRESS, PORT)
else:
    conn = pwn.process(['python3', 'challenge1.py'])

# Retrieve the encrypted Flag c = t^e mod n
conn.recvuntil(b":")
flag = int((conn.recvline(keepends=False)).decode())
print("Encrypted Flag (c): ", flag)
c = flag

# Set parameters used for the malleability attack
e = 65537
g = 2

# Get c_a = g^e mod n
conn.recvuntil(b"> ")
conn.sendline(b"1")

conn.recvuntil(b"> ")
conn.sendline(long_to_bytes(g))

conn.recvuntil(b":" )
c_a = int(conn.recvline(keepends=False).decode())

print("Ca: ", c_a)

# Compute c_b = c * c_a
c_b = c * c_a
print("Cb: ", c_b)

# Send c_b to the server
conn.recvuntil(b"> ")
conn.sendline(b"2")

conn.recvuntil(b"> ")
conn.sendline(str(c_b).encode())

# Get m from the server. m = c_b^d mod n = (c * c_a)^d mod n = t * g
conn.recvuntil(b": ")
m = int(conn.recvline(keepends=False).decode())

print("M: ", m)

# Compute t from m
t = m // g
print("T: ", t)
print("Flag: ", long_to_bytes(t).decode())
