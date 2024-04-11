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

# Retrieve the encrypted Flag c = s^e mod n
conn.recvuntil(b":")
flag = int((conn.recvline(keepends=False)).decode())
print("Encrypted Flag (c): ", flag)
c = flag

# Set parameters used for the malleability attack
e = 65537
betha = 2

# Get alpha = betha^e mod n
conn.recvuntil(b"> ")
conn.sendline(b"1")

conn.recvuntil(b"> ")
conn.sendline(long_to_bytes(betha))

conn.recvuntil(b":" )
alpha = int(conn.recvline(keepends=False).decode())

print("Alpha: ", alpha)

# Compute C = c * alpha
C = c * alpha
print("C: ", C)

# Send C to the server
conn.recvuntil(b"> ")
conn.sendline(b"2")

conn.recvuntil(b"> ")
conn.sendline(str(C).encode())

# Get m from the server. m = C^d mod n = (c * alpha)^d mod n = s * betha
conn.recvuntil(b": ")
m = int(conn.recvline(keepends=False).decode())

print("M: ", m)

# Compute s from m. Notice how we use // (rather than / followed
# by a cast) in order to get a higher precision in the division
s = m // betha
print("S: ", s)
print("Flag: ", long_to_bytes(s).decode())
