import pwn
from Crypto.Util.number import bytes_to_long, long_to_bytes

REMOTE = False
DEBUG = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 10500

conn = pwn.remote(IP_ADDRESS, PORT)

conn.recvuntil(b"you: ")
msg = conn.recvuntil(b"!")
print(msg)

msg_int = bytes_to_long(msg)
#print(msg_int)

conn.recvuntil(b"?")
conn.sendline(str(msg_int).encode())

conn.recvuntil(b": ")
p = int(conn.recvline(keepends=False))
conn.recvuntil(b": ")
q = int(conn.recvline(keepends=False))

n = p * q

conn.recvuntil(b"?")
conn.sendline(str(n).encode())

phi = (p-1)*(q-1)

conn.recvuntil(b"?")
conn.sendline(str(phi).encode())

e = 65537
d = pow(e, -1, phi)

conn.recvuntil(b"?")
conn.sendline(str(d).encode())

msg_encr = pow(msg_int, e, n)

conn.recvuntil(b"?")
conn.sendline(str(msg_encr).encode())

conn.recvuntil(b": ")
flag_enc = conn.recvline()
print(flag_enc)

flag = pow(int(flag_enc), d, n)
print(long_to_bytes(flag).decode())


