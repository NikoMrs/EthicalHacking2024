import pwn
from Crypto.Util.number import bytes_to_long, long_to_bytes
import hlextend

REMOTE = False

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 10201

conn = pwn.remote(IP_ADDRESS, PORT)

conn.recvuntil(b"> ")
conn.sendline(b"1")

conn.recvuntil(b"> ")
conn.sendline(b"username")

conn.recvuntil(b"> ")
conn.sendline(b"")

conn.recvuntil(b": ")
token = conn.recvline(keepends=False)

conn.recvuntil(b": ")
psw = conn.recvline(keepends=False)

print("Signup completed")

token = "||||richperson".encode()

sha = hlextend.new('sha1')
password = hlextend.extend()

sha.extend(b'||||richperson', token, 32, )

conn.recvuntil(b"> ")
conn.sendline(b"2")

conn.recvuntil(b"> ")
conn.sendline(token)

conn.recvuntil(b"> ")
conn.sendline(psw)

conn.interactive()


